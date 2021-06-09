from flask import Flask, render_template, abort, request, session, url_for, redirect, flash, g
from os import environ
from datetime import timedelta
import sqlite3
from pathlib import Path

app = Flask(__name__)

# SESSION KEY
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', '1234')

# DB
DATABASE_PATH = Path(__file__).parent / 'data/login.db'


# SET CONNECTION WITH DB
def get_db():
    if not hasattr(g, 'conn'):
        app.logger.debug(f"» New Connection requested from endpoint '{request.endpoint}'")
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        setattr(g, 'conn', conn)
    return g.conn


# TERMINATE CONNECTION WITH DB
@app.teardown_appcontext
def close_connection(ctx):
    '''
    Close connection on appcontext teardown
    This will fire whether there was an exception or not
    '''
    if conn := g.pop('conn', None):
        app.logger.debug('» Teardown AppContext')
        app.logger.debug('» Connection closed')
        conn.close()


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
        'login/login.html',
        usernameCookie=request.cookies.get('user')
    )


@app.post('/login')
def sign_in():
    errors = []

    # get form values
    formUsername = request.form.get('username')
    formPassword = request.form.get('password')

    # validation with DB
    # check for username existance
    cur = get_db().cursor()
    checkLogin = cur.execute(
        '''
        SELECT [username], [password]
        FROM [user]
        WHERE [username] = :username
        ''',
        {'username': formUsername}
    ).fetchone()
    cur.close()
    # user exists
    if checkLogin:
        # password is incorrect
        if checkLogin['password'] != formPassword:
            errors.append({'field': 'password'})
    else:
        # username does not exist
        errors.append({'field': 'username'})
        errors.append({'field': 'password'})
    # if username or/and password is incorrect -> error
    if errors:
        flash('Invalid Credentials. Please try again.', 'error')
        return render_template('login/login.html', errors=errors)
    else:
        # initialize a session
        session['username'] = formUsername
        # set session to be alive even when you close the browser
        session.permanent = True
        # set session timeout to 10 days (flask default 31days)
        app.permanent_session_lifetime = timedelta(minutes=10)
        flash('You were successfully logged in.', 'success')
        # set cookie for username (set cookie before redirect)
        url = session['url'] if 'url' in session else url_for('home')
        rdr = redirect(url)
        rdr.set_cookie('user', formUsername, max_age=timedelta(minutes=10))
        return rdr


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
    # check for username existance
    cur = get_db().cursor()
    usernameExists = cur.execute(
        '''
        SELECT [username]
        FROM [user]
        WHERE [username] = :username
        ''',
        {'username': username}
    ).fetchone()
    cur.close()
    if usernameExists:
        # redirect to login if not signed in and username exists
        if 'username' not in session:
            # save url endpoint and args for redirection from login
            session['url'] = url_for('profile', username=username)
            return redirect(url_for('show_login_form'))
        # check if user should have access to this profile
        if username == session['username']:
            app.logger.debug(username)
            # User Data (from DB)
            cur = get_db().cursor()
            data = cur.execute(
                '''
                SELECT [username],
                    [first_name],
                    [last_name],
                    [email],
                    [nationality],
                    [mobile],
                    [about],
                    [last_login]
                FROM [user]
                WHERE [username] = :username
                ''',
                {"username": username}
            ).fetchone()
            cur.close()
            # Interests of this user
            cur = get_db().cursor()
            interests = cur.execute(
                '''
                SELECT i.id, i.description
                FROM [user] u
                INNER JOIN [user_interest] ui ON u.username = ui.user_username
                INNER JOIN [interest] i ON ui.interest_id = i.id
                WHERE u.username = :username
                ''',
                {'username': username}
            ).fetchall()
            cur.close()
            app.logger.debug(interests)
        else:
            abort(401)
    else:
        abort(404)
    # Render profile page
    return render_template(
        'profile/profile.html',
        profileData=data,
        interests=interests,
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
