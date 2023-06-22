from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    # Data otentikasi akun
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # Data diri
    nama_lengkap = db.Column(db.String(200), nullable=True, default="")
    range_gaji = db.Column(db.Integer, nullable=True, default=0)
    kordinat_longitude_tempat_kerja = db.Column(
        db.String(50), nullable=True, default=""
    )
    kordinat_latitude_tempat_kerja = db.Column(db.String(50), nullable=True, default="")

    # profile komplit
    is_filled = db.Column(db.Boolean, nullable=False, default=False)


class Kecamatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_kecamatan = db.Column(db.String(50), nullable=False, default="")


class Rumah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gambar = db.Column(db.String(200), nullable=True, default="")
    alamat = db.Column(db.String(500), nullable=False, default="")
    nama_perumahan = db.Column(db.String(200), nullable=False, default="")
    harga = db.Column(db.Integer, nullable=False, default="")
    kecamatan = db.Column(db.String(100), nullable=True, default="")
    latitude = db.Column(db.String(100), nullable=True, default="")
    longitude = db.Column(db.String(100), nullable=True, default="")
    kontak_agen = db.Column(db.String(100), nullable=True, default="")
    fasilitas = db.Column(db.String(500), nullable=False, default="")
    luas = db.Column(db.Integer, nullable=False, default=0)
    lantai = db.Column(db.Integer, nullable=False, default=0)
    kamar_tidur = db.Column(db.Integer, nullable=False, default=0)
    kamar_mandi = db.Column(db.Integer, nullable=False, default=0)
    njop = db.Column(db.Integer, nullable=False, default=0)


class Agen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_agen = db.Column(db.String(100), nullable=False, default="")
    nomor_telepon = db.Column(db.String(100), nullable=False, default="")
    email = db.Column(db.String(100), nullable=False, default="")
    whatsapp = db.Column(db.String(100), nullable=False, default="")
