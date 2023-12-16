from flask import render_template, Blueprint

error = Blueprint('error', __name__, url_prefix='/')

@error.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404