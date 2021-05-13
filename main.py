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
    return render_template(
        'login/login.html'
    )


# Logout Route
@app.route('/logout')
def logout():
    return 'Ok'


# Profile Route
@app.route('/profile/<string:username>')
def profile(username):

    # User Data (from DB)
    data = {
        'fullname': 'Noah Tremblay',
        'username': username,
        'email': 'noah_trembl01@gmail.com',
        'nationality': 'Canadian',
        'mobile': '6967854895',
        'about': '''Lorem ipsum dolor sit amet consectetur adipisicing elit.
        Eius commodi veniam placeat voluptatum totam voluptate quo suscipit
        non ex um.''',
        'interests': ['Food', 'Football', 'Cooking', 'Running']
    }

    # Render profile page
    return render_template(
        'profile/profile.html',
        profileData=data,
    )


# Error Pages (for testing)
@app.route('/error/<int:errorCode>')
def error(errorCode):

    # Coresponging messages to error codes
    errCodeDict = {
        404: "Page Not Found",
        401: "Unauthorized access"
    }

    return render_template(
        f'error/{errorCode}.html',
        errorCode=errorCode,
        errorMessage=errCodeDict[errorCode]
    )
