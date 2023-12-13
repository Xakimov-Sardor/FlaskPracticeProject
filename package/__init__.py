from flask import Flask
from os import path, mkdir

def create_app():
    
    app = Flask(__name__)

    # configuring app

    app.config.from_mapping(
        SECRET_KEY = 'nothing bro',
        DATABASE = path.join(app.instance_path, 'database.sql') # example path for database
    )
    # The from_mapping function allows updating multiple values at once and ignores lowercase keys.

    # creating instance(for database) folder
    try:
        mkdir(app.instance_path)
    except:...
   

    from .db import init_app
    init_app(app)
    

    return app