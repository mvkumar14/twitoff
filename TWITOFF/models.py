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

class Tweet(DB.Model):
    """Tweets we pull"""
    id = DB.Column(DB.BigInteger,primary_key=True)
    text = DB.Column(DB.Unicode(280))
