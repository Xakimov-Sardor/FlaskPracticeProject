import sqlite3

import click as cmd
from flask import current_app as app, g, Flask

import colorama
colorama.init()
# func for get database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            database=app.config['DATABASE'], # path database file
            detect_types=sqlite3.PARSE_DECLTYPES, # for detect data type
        )
        g.db.row_factory = sqlite3.Row # allows you to get information from the database in the form of a dict
    return g.db

def close_db(e=None):
    "for close database if exists"
    db = g.pop('db', -1)
    if db != -1:
        print(f'{colorama.Fore.RED} Database closed')
        db.close()

def init_db():
    db = get_db()

    with app.open_resource('scheme.sql') as file:
        db.executescript(file.read().decode('utf8'))

@cmd.command('init-database')
def init_db_cmd():
    
    init_db()

    cmd.echo(f'{colorama.Fore.GREEN} Database was successfully created')

def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_cmd)


