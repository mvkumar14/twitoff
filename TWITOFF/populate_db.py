# Write methods to pull actual Users and Tweets and replace your invented data with actual Twitter data
# Add an embedding field to your Tweet model, and functions to populate it with embeddings returned from Basilica


from .twitter import *
from .models import DB, User, Tweet

# I'm going to start out with a simple version that only
# deals with deleting the database and adding in these user
def create_default_db():
    DB.drop_all()
    DB.create_all()

    # Change this value to be able to change what gets inserted into the Database
    pull_users = ['elonmusk','vgr','nasa','ILMVFX','neiltyson']

    for i in pull_users:
        twitter_user = TWITTER.get_user(i)
        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended')
        db_user = User(id=twitter_user.id,name=twitter_user.name,newest_tweet_id=tweets[0].id)
        for a in tweets:
            embedding = BASILICA.embed_sentence(a.full_text, model='twitter')
            db_tweet = Tweet(id=a.id, text=a.full_text, user_id=twitter_user.id,
                embedding=embedding)
            DB.session.add(db_tweet)
        DB.session.add(db_user)

    DB.session.commit()



# Get all the users from the DATABASE

# If pull_users in set users then delete from pull_users

#maybe make this a function accessible from within the command line?
