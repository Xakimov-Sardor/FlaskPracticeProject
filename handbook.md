# Project Layout(optional, but better)
    FlaskProject/
        ├── package
            ├── __init__.py
            ├── auth.py
            ├── views.py
            ├── db.py
            ├── scheme.sql
            ├── templates/
                ├── auth/
                    ├── signup.html
                    ├── login.html
                    ├── logout.html <!--optional-->
                ├── views/
                    ├── home.html
                ├── base.html
            ├── static/
                ├── style.css
        ├── pyproject.toml <!-- a bit advanced -->
        ├── MANIFEST.in
# Application setup for beginners
    1.create __init__ file
    2.create create_app function
    3.import flask object and creat it as app
    4.configure app

