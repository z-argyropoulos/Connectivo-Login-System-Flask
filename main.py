from flask import Flask, render_template

app = Flask(__name__)


# Root Route
@app.route('/')
def home():

    # Signed In test values
    signedIn = True      # False
    username = 'Noah_Tremblay'      # ''

    return render_template(
        'root/index.html',
        signedIn=signedIn,
        username=username
    )


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
