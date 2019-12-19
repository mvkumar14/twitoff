"""Code for our app"""


from decouple import config
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user
from .populate_db import create_default_db
from .predict import predict_user

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

    @app.route('/defaults')
    def defaults():
        create_default_db()
        return render_template('base.html', title='Defaults Set', users=[])


    # POST is when you are submitting data
    # GET is when you receive data
    @app.route('/user',methods=['POST'])
    @app.route('/user/<name>',methods=['GET'])
    def user(name=None,message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message="User {} successfully added".format(name)
            # User here is accessing the database
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message =  'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
        message=message)

    @app.route('/compare', methods = ['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
            request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1,user2, request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction:',
            message=message)
    @app.route('/echo',methods =['POST','GET'])
    def echo():
        print(request.values['echo_box'])
        return render_template('echo.html',title='echo echo',users=[])





    return app
# You can edit the above to be able to create new routes with
# functionality that you choose to the functions in this file.
