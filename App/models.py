from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    # Data otentikasi akun
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    # Data diri
    nama_lengkap = db.Column(db.String(200), nullable=True, default="")
    range_gaji = db.Column(db.Integer, nullable=True, default=0)
    kordinat_longitude_tempat_kerja = db.Column(
        db.String(50), nullable=True, default=""
    )
    kordinat_latitude_tempat_kerja = db.Column(db.String(50), nullable=True, default="")

    # profile komplit
    is_filled = db.Column(db.Boolean, nullable=False, default=False)
