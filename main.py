from flask import Flask
app = Flask(__name__)


# Root Route
@app.route('/')
def home():
    return 'Home page'


# Login Route
@app.route('/login')
def login():
    return 'Login form'


# Logout Route
@app.route('/logout')
def logout():
    return 'Ok'


# Profile Route
@app.route('/profile/<string:username>')
def profile(username):
    return username
