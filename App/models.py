from . import db
from flask_login import UserMixin


# file ORM untuk kerangka database
class User(db.Model, UserMixin):
    # Data otentikasi akun
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # Data diri
    nama_lengkap = db.Column(db.String(200), nullable=True, default="")
    range_gaji = db.Column(db.Integer, nullable=True, default=0)
    alamat_tempat_kerja = db.Column(db.String(300), nullable=False, default="")

    # profile komplit
    is_filled = db.Column(db.Boolean, nullable=False, default=False)
    selesai_loading_jarak = db.Column(db.Boolean, nullable=False, default=False)


class Kecamatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_kecamatan = db.Column(db.String(50), nullable=False, default="")


class Rumah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gambar = db.relationship("GambarRumah", backref="gambar_rumah")
    alamat = db.Column(db.String(500), nullable=False, default="")
    nama_perumahan = db.Column(db.String(200), nullable=False, default="")
    harga = db.Column(db.Integer, nullable=False, default=0)
    kecamatan = db.Column(db.String(100), nullable=True, default="")
    latitude = db.Column(db.String(100), nullable=True, default="")
    longitude = db.Column(db.String(100), nullable=True, default="")
    kontak_agen = db.Column(db.String(100), nullable=True, default="")
    kontak_agen_id = db.Column(db.Integer, nullable=True, default="")
    agen_nomor_telepon = db.Column(db.String(100), nullable=False, default="")
    agen_email = db.Column(db.String(100), nullable=True, default="")
    agen_whatsapp = db.Column(db.String(100), nullable=True, default="")
    categori_fasilitas = db.Column(db.String(500), nullable=True, default="")
    fasilitas = db.Column(db.String(500), nullable=True, default="")
    luas = db.Column(db.Integer, nullable=False, default=0)
    lantai = db.Column(db.Integer, nullable=False, default=0)
    kamar_tidur = db.Column(db.Integer, nullable=False, default=0)
    kamar_mandi = db.Column(db.Integer, nullable=False, default=0)
    njop = db.Column(db.Integer, nullable=True, default=0)
    click_count = db.Column(db.Integer, nullable=True, default=0)
    deskripsi = db.Column(db.String(10000), nullable=False, default="")


class GambarRumah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_gambar = db.Column(db.String(500), nullable=False, default="")
    rumah = db.Column(db.Integer, db.ForeignKey("rumah.id"))


class Agen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_agen = db.Column(db.String(100), nullable=False, default="")
    nomor_telepon = db.Column(db.String(100), nullable=False, default="")
    email = db.Column(db.String(100), nullable=False, default="")
    whatsapp = db.Column(db.String(100), nullable=False, default="")


class FixedBunga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fixed_bunga = db.Column(db.Integer, nullable=False, default=0)
