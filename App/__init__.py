from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

import os
import pandas as pd
import locale


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
    datasets_to_database(app)

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


# read datasets from datasets folder, read and put it in the database
def datasets_to_database(app):
    from .models import Rumah
    from .models import Kecamatan
    from .models import Agen

    locale.setlocale(locale.LC_ALL, "id_ID")

    if os.path.exists(f"App/datasets/houses_dummy_datasets.json"):
        df = pd.read_json(os.path.join(f"App/datasets/houses_dummy_datasets.json"))

        with app.app_context():
            for _, rs in df.iterrows():
                kontak_agen = dict(rs[9])
                kordinat = dict(rs[8])

                new_rumah_data = Rumah(
                    alamat=str(rs[0]),
                    nama_perumahan=str(rs[1]),
                    luas=int(rs[2]),
                    harga=rs[3],
                    lantai=int(rs[4]),
                    kamar_tidur=int(rs[5]),
                    kamar_mandi=int(rs[6]),
                    kecamatan=str(rs[7]),
                    latitude=kordinat["latitude"],
                    longitude=kordinat["longitude"],
                    kontak_agen=str(kontak_agen["nama"]),
                    fasilitas=", ".join(rs[11]),
                    njop=int(rs[10]),
                )
                db.session.add(new_rumah_data)
            db.session.commit()

            for _, rs in df.iterrows():
                to_check_kecamatan = Kecamatan.query.filter_by(
                    nama_kecamatan=str(rs[7])
                ).first()

                if not to_check_kecamatan:
                    new_kecamatan = Kecamatan(nama_kecamatan=str(rs[7]))
                    db.session.add(new_kecamatan)
            db.session.commit()

            for _, rs in df.iterrows():
                kontak_agen = dict(rs[9])

                to_check_agen = Agen.query.filter_by(
                    nama_agen=kontak_agen["nama"]
                ).first()
                if not to_check_agen:
                    new_agen = Agen(
                        nama_agen=kontak_agen["nama"],
                        nomor_telepon=kontak_agen["nomor_telepon"],
                        email=kontak_agen["email"],
                        whatsapp=kontak_agen["nomor_whatsapp"],
                    )
                    db.session.add(new_agen)
                db.session.commit()

        os.rename(
            os.path.join(f"App/datasets/houses_dummy_datasets.json"),
            os.path.join(f"App/datasets/houses_dummy_datasets_DONE.json"),
        )
        print("[+] berhasil menambahkan dataset ke database")
        return

    print("[-] dataset sudah ada dalam database")
    return
