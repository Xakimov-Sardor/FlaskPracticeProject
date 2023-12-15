from flask import Blueprint, render_template, session

views = Blueprint('views', __name__, url_prefix='/')



@views.route('/')
@views.route('/home')
def home():
    a = session.get('user_id')
    return render_template('views/home.html')

