from flask import Flask, render_template, abort, request, session, url_for, redirect, flash
from os import environ
from datetime import timedelta

app = Flask(__name__)

# SESSION KEY
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', '1234')


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
    # if user is signed in already then send him to homepage
    if 'username' in session:
        return redirect(url_for('home'))

    # otherwise show form to sign in
    return render_template(
        'login/login.html'
    )


@app.post('/login')
def sign_in():
    errors = []

    # get form values
    username = request.form.get('username')
    password = request.form.get('password')

    # validation with DB
    # error with username
    """ errors.append({'field': 'username'}) """
    # error with password
    """ errors.append({'field': 'password'}) """

    if errors:
        flash('Invalid Credentials. Please try again.', 'error')
        return render_template('login/login.html', errors=errors)
    else:
        # initialize a session
        session['username'] = username
        # set session to be alive even when you close the browser
        session.permanent = True
        # set session timeout to 10 days (flask default 31days)
        app.permanent_session_lifetime = timedelta(minutes=10)
        flash('You were successfully logged in.', 'success')
        return redirect(url_for('home'))


# Logout Route
@app.route('/logout')
def logout():
    """ clear all session keys
    use this method as
    session.clear() would clear flash messages
    before displaying after session.clear()"""
    for key in list(session.keys()):
        session.pop(key)
    flash('Successfully logged out.', 'info')
    return redirect(url_for('home'))


# Profile Route
@app.route('/profile/<string:username>')
def profile(username):
    # check if user should have access to this profile
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
