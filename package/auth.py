from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db
import functools
auth = Blueprint('auth', __name__, url_prefix='/')


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = None

        db = get_db()

        if len(username) < 3:
            error = ('username must be at least 3 characters long', 'error')
        elif len(password) < 8:
            error = ('password must be at least 8 characters long', 'error')
        
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password, 'scrypt')))
                db.commit()
                
            except db.IntegrityError:
                error = f"User {username} is already registered."
            finally:
                return redirect(url_for('views.home'))
        flash(error)
        
    return render_template('auth/signup.html')
@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password  = request.form.get('password')
        db = get_db()

        error = None

        user = db.execute(
            'SELECT * FROM  user WHERE username = ?',
            (username, )
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']

        flash(error)
    return render_template('auth/login.html')


@auth.before_app_request
def load_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        )

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view