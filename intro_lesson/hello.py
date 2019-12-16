"""Minimal flask app"""

from flask import Flask, render_template

# Make the application
app = Flask(__name__)

# Make the route
@app.route('/')

# Now define a function
def hello():
    return "Hello World!"
# The page returns text

# Make a second route
@app.route('/about')

# Define new function
def preds():
    return render_template('about.html')
# The page returns a template
# render_templates is built to find a folder called templates
# in your main directory.
