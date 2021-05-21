from flask import Flask, render_template, abort

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
    if username != 'Noah_Tremblay':  # For testing purposes
        abort(401)

    # User Data (from DB)
    data = {
        'fullname': 'Noah Tremblay',
        'username': username,
        'email': 'noah_trembl01@gmail.com',
        'nationality': 'can',        # Canada -> can (in future dictionary)
        'mobile': '6967854895',
        'about': '''Lorem ipsum dolor sit amet consectetur adipisicing elit.
        Eius commodi veniam placeat voluptatum totam voluptate quo suscipit
        non ex um.''',
        'interests': ['Cooking', 'Football', 'Volunteering', 'Running'],
        'last-seen': '5 mins ago'     # in future function date -> elapsed time
    }

    # Render profile page
    return render_template(
        'profile/profile.html',
        profileData=data,
        username=username
    )


# 401 ERROR HANDLER (UNAUTHORIZED ACCESS)
@app.errorhandler(401)
def unauthorized_error_page(e):
    return render_template(
        'error/401.html',
        errorCode=401,
        errorMessage="Unauthorized Access"
    ), 401


# 404 ERROR HANDLER (PAGE NOT FOUND)
@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'error/404.html',
        errorCode=404,
        errorMessage="Page Not Found"
    ), 404
