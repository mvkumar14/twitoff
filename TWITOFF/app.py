"""Code for our app"""


from decouple import config
from flask import Flask, render_template, request
from .models import DB, User

# We are creating an app factory
def create_app():
    app = Flask(__name__)

    # Add config for database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    # To get rid of the depreciation warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Have the database know about the app
    DB.init_app(app)

    # Create new route
    @app.route('/')

    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset', users=[])

    return app
# You can edit the above to be able to create new routes with
# functionality that you choose to the functions in this file.
