from flask import Blueprint, render_template, flash, request, g, redirect, url_for, abort
from package.auth import login_required
from package.db import get_db

views = Blueprint('views', __name__, url_prefix='/')



@views.route('/')
@views.route('/home')
def home():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('views/home.html', posts=posts)

@views.route('/create', methods=['POST','GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        error = None
        db = get_db()

        if len(title) < 2:
            error = 'Maqola sarlavhasi kamida 2 ta belgiganda iborat bo\'lishi kerak'
            flash(error)
        elif len(body) < 10:
            error = 'Ko\'proq malumot yozing'
            flash(error)
        else:
            post = db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.current_user['id'])
            )
            db.commit()

            return redirect(url_for('views.home'))



    return render_template('views/create_blog.html')


def get_post(id: int, check_author: bool = True):
    post = get_db().execute(
        'SELECT * FROM post WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Bu {id} bilan post mavjud emas")
    else:
        if check_author and post['author_id'] != g.current_user['id']:
            abort(403, f"Muallifni hurmat qilaylik")

    return post


@views.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if len(title) < 2:
            error = 'Maqola sarlavhasi kamida 2 ta belgiganda iborat bo\'lishi kerak'
            flash(error)
        elif len(body) < 10:
            error = 'Ko\'proq malumot yozing'
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?, id= ?",
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('views.home'))
        
    return render_template('views/update_blog.html', post=post)

@views.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = get_post(id)

    db = get_db()
    db.execute(
        "DELETE FROM post WHERE id = ?",
        (id, )
    )
    db.commit()

    return redirect(url_for('views.home'))

