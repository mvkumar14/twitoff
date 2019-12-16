"""Code for our app"""



from flask import Flask
from .models import DB

# We are creating an app factory
def create_app():
    app = Flask(__name__)

    # add config for database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    # have the database know about the app
    DB.init_app(app)


    @app.route('/')
    def root():
        return "Welcome to twitoff"
    return app
# You can edit the above to be able to create new routes with
# functionality that you choose to the functions in this file.
