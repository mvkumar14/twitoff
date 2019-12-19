""" Retrieve tweets, embedding, save into database """

import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(config('BASILICA_KEY'))

# to do - add functions that use basilica

def add_or_update_user(username):
    """
    Add or update a user in the database, and their tweets, or
    else give an error
    """
    try:
        # connect to twitter api and get user
        twitter_user = TWITTER.get_user(username)

        # either you update or you get the user.
        db_user = (User.query.get(twitter_user.id) or
            User(id=twitter_user.id,name=username))

        # add user to database
        DB.session.add(db_user)

        # pulling tweets from user (twitter api)
        tweets = twitter_user.timeline(count=200,exclude_replies=True,
            include_rts=False, tweet_mode='extended',
            since_id=db_user.newest_tweet_id)

        # if we grabbed tweets
        if tweets:
            # update newest tweet id
            db_user.newest_tweet_id= tweets[0].id
        for tweet in tweets:
            # calculate the embedding on the full tweets
            embedding = BASILICA.embed_sentence(tweet.full_text,
                model='twitter')
            db_tweet = Tweet(id=tweet.id,text=tweet.full_text[:300],
            embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
        pass
    except Exception as e:
        print(f'Error processing {username}: {e}')
    else:
        DB.session.commit()
