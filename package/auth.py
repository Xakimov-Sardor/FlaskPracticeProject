from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        if len(username) < 3:
            error = 'Foydalanuvchi nomi kamida 3 ta belgidan iborat bo\'lishi kerak'
        elif len(password) < 8:
            error = 'Iltimos kuchliroq parol o\'rnatish'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password, 'scrypt'))
                )
                db.commit()
                user = db.execute(
                    "SELECT * FROM user WHERE username = ?",
                    (username, )
                ).fetchone()
                session.clear()
                session['user_id'] = user['id']

                
                print(f'{username} ok')
            except db.IntegrityError:
                error = 'Bu foydalanuvchi nomi band'
                print(f'{username} already exist')
            else:
                print('ok all')
                return redirect(url_for('views.home'))   
                    
    return render_template('auth/signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE username = ?",
            (username, )
        ).fetchone()

        if len(username) < 3 and   len(password) < 8:
            error = 'Foydalanuvchi nomi yoki parol xato'
            flash(error)
            print(error)

        else:
            if user:
                if  check_password_hash(user['password'], password):
                    session.clear()
                    session['user_id'] = user['id']
                    print('login ok | cookie ok')
                    return redirect(url_for('views.home'))
                else:
                    error = 'Foydalanuvchi nomi yoki parol xato'
                    flash(error)
                    print(error)
        

    return render_template('auth/login.html')
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth.before_app_request
def load_user_from_id():
    user_id = session.get('user_id')

    if user_id is None:
        g.current_user = None
    else:
        g.current_user = get_db().execute(
            "SELECT * FROM user WHERE id = ?",
            (user_id, )
        ).fetchone()

def login_required(view):
    import functools
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view