from flask import Blueprint, render_template, session

views = Blueprint('views', __name__, url_prefix='/')



@views.route('/')
@views.route('/home')
def home():
    return render_template('views/home.html')

