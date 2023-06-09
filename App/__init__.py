from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin


import os
import pathlib


app = Flask(__name__)
csrf = CSRFProtect()
db = SQLAlchemy()

DB_NAME = "database.db"


def start_app():
    # application config
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "katakakekukukukakikakakukakukenapaku6969"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    # login manager
    login_manager = LoginManager()
    login_manager.login_view = "public_auth.handle_login"
    login_manager.init_app(app)
    login_manager.login_message = "Silahkan login terlebih dahulu."

    # database
    db.init_app(app)
    from .models import User

    # blueprint import
    from .admin_views import admin_views
    from .admin_auth import admin_auth
    from .public_views import public_views
    from .public_auth import public_auth

    app.register_blueprint(admin_views, url_prefix="/")
    app.register_blueprint(admin_auth, url_prefix="/")
    app.register_blueprint(public_views, url_prefix="/")
    app.register_blueprint(public_auth, url_prefix="/")

    # cross site request forgery protection
    csrf.init_app(app)

    # create app
    create_database(app)

    return app


def create_database(app):
    if not os.path.exists("App/" + DB_NAME):
        db.create_all(app=app)
        print("[+] database succesfully generated!")
    print("[-] database already generated!")
