from flask import Flask, render_template, abort, request, session, url_for, redirect
from os import environ
from datetime import datetime

app = Flask(__name__)

# SESSION KEY
app.secret_key = b'\xd1s}\xa2m\xbf\xa8\x12`0\xecR^\x14\xc7e\xfa\nr\xb2\x82\xc8\xdf'


# Root Route
@app.route('/')
def home():
    return render_template(
            'root/index.html',
            username=(session['username'] if 'username' in session else None)
    )


# Login Route
@app.get('/login')
def show_login_form():
    return render_template(
        'login/login.html'
    )


@app.post('/login')
def sign_in():
    loginError = False
    """ get form values """
    username = request.form.get('username')
    password = request.form.get('password')

    """ validation with DB  """
    session['username'] = username

    if loginError:
        app.logger.debug('Sign in error')
        return render_template('login/login.html')
    else:
        session['username'] = username
        return redirect(url_for('home'))


# Logout Route
@app.route('/logout')
def logout():
    """ clear all session keys
    use this method as
    session.clear() would clear flash messages
    before displaying after session.clear()"""
    for key in list(session.keys()):
        session.pop('username')
    return redirect(url_for('home'))


# Profile Route
@app.route('/profile/<string:username>')
def profile(username):

    """ check if user should have access to this profile """
    if username == session['username']:
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
    else:
        abort(401)

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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=environ.get('SERVER_PORT', 5000))
