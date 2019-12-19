""" Everything related to the structure of the database """

from flask_sqlalchemy import SQLAlchemy

# Global variable, an object of type sqlalchmy()?
DB = SQLAlchemy()

# There are going to be two tables
# one for users ,and one for tweets, and we are going organize
# with classes

# parent class for both classes is DB.Model
# We can look at source for DB.Model from sqlalchemy

class User(DB.Model):
    """ Twitter users that we analyze"""
    id = DB.Column(DB.BigInteger,primary_key=True)
    name = DB.Column(DB.String(15),nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)
    def __repr__(self):
        return '<User {}>'.format(self.name)

class Tweet(DB.Model):
    """Tweets we pull"""
    id = DB.Column(DB.BigInteger,primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # The relationship between user and tweets is one to many, which is why the backlink
    # is "tweets" instead of "tweet". If you wanted to properly convey a
    # many to many relationship you might want to do a backfill from both ends
    # referencing the other end in the plural form.
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    # Now this means that whenever new tweets are generated are added to the database
    # you have to add the embedding too! (The processing time can be upfront, and then)
    # comparisons can be made quickly.
    embedding = DB.Column(DB.PickleType,nullable=False)
    def __repr__(self):
        return '<Tweet {}>'.format(self.text)
