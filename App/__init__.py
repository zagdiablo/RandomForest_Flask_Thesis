from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

import os


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
    login_manager.login_view = "public_auth.login_page"
    login_manager.init_app(app)
    login_manager.login_message = "Silahkan login terlebih dahulu."

    # database
    from .models import User

    db.init_app(app)

    # blueprint import
    from .admin_views import admin_views
    from .admin_auth import admin_auth
    from .public_views import public_views
    from .public_auth import public_auth
    from .public_views_loggedin import public_views_loggedin

    app.register_blueprint(admin_views, url_prefix="/")
    app.register_blueprint(admin_auth, url_prefix="/")
    app.register_blueprint(public_views, url_prefix="/")
    app.register_blueprint(public_auth, url_prefix="/")
    app.register_blueprint(public_views_loggedin, url_prefix="/")

    # cross site request forgery protection
    csrf.init_app(app)

    # login manager initiation
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # generate database
    create_database(app)
    generate_admin_account(app)

    return app


def create_database(app):
    if not os.path.exists(f"App/{DB_NAME}"):
        db.create_all(app=app)
        print(f"[+] Database successfully created!")
        return
    print(f"[-] Dabase already exist!")


def generate_admin_account(app):
    with app.app_context():
        from .models import User

        master_admin_account = User.query.get(1)

        if not master_admin_account:
            generate_admin = User(
                email="admin@admin.com",
                password=generate_password_hash("admin", "sha256"),
                is_admin=True,
            )
            db.session.add(generate_admin)
            db.session.commit()
            print("[+] berhasil membuat akun admin master")
            return

        print("[-] akun admin master sudah ada")
        return
