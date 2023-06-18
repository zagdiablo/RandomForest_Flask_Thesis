from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from .models import User
from . import db


#####
# file ini menghandle tampilan halaman yang tidak membutuhkan user login
#####


public_views = Blueprint("public_views", __name__)


#
#
# API untuk handle inisialisasi keperluan webapp
@public_views.route("/", methods=["GET"])
def init():
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
        return redirect("/home")

    print("[-] akun admin master sudah ada")
    return redirect("/home")


#
#
# API untuk handle halaman home
@public_views.route("/home", methods=["GET"])
def home_page():
    user_is_authenticated = current_user.is_authenticated

    return render_template(
        "public/home.html", user_is_authenticated=user_is_authenticated
    )


#
#
# API untuk handle halaman pencarian rumah
@public_views.route("/cari_rumah", methods=["GET"])
def cari_rumah_page():
    user_is_authenticated = current_user.is_authenticated

    return render_template(
        "public/cari_rumah.html", user_is_authenticated=user_is_authenticated
    )


@public_views.route("/handle_cari_rumah", methods=["POST"])
def handle_cari_rumah():
    kecamatan = request.form.get("search_bar_by_kecamatan")
    dropdown_lantai = request.form.get("dropdown_lantai")
    dropdown_luas = request.form.get("dropdown_luas")
    dropdown_kamar_tidur = request.form.get("dropdown_kamar_tidur")
    dropdown_kamar_mandi = request.form.get("dropdown_kamar_mandi")
    dropdown_harga = request.form.get("dropdown_harga")
    checbox_gym = request.form.get("checkbox_gym")
    checkbox_masjid = request.form.get("checkbox_masjid")
    checkbox_kamar = request.form.get("checkbox_kamar")
    checkbox_taman = request.form.get("checkbox_taman")
    checkbox_playground = request.form.get("checkbox_playground")
    checkbox_kolam_renang = request.form.get("checkbox_kolam_renang")

    # TODO pengolahan data dan rekomendation system
    print(
        kecamatan,
        dropdown_lantai,
        dropdown_luas,
        dropdown_kamar_tidur,
        dropdown_kamar_mandi,
        dropdown_harga,
        checbox_gym,
        checkbox_masjid,
        checkbox_kamar,
        checkbox_taman,
        checkbox_playground,
        checkbox_kolam_renang,
    )

    return redirect("/cari_rumah")


@public_views.route("/get_price_suggestion", methods=["POST"])
def get_price_suggestion():
    #####
    # TODO handle logika machine learning & query data hasil
    # TODO requirement: untuk user yang belum login range parameter gaji dan kontak sales rumah di tiadakan
    lantai = request.form.get("lantai")
    ukuran = request.form.get("ukuran")
    print(lantai, ukuran)
    #####

    return redirect("/cari_rumah")


#
#
# API untuk handle halaman tentang kami
@public_views.route("/about", methods=["GET"])
def about_page():
    user_is_authenticated = current_user.is_authenticated

    return render_template(
        "public/about.html", user_is_authenticated=user_is_authenticated
    )


#
#
# API untuk handle halaman kontak
@public_views.route("/contact", methods=["GET"])
def contact_page():
    user_is_authenticated = current_user.is_authenticated

    return render_template(
        "public/contact.html", user_is_authenticated=user_is_authenticated
    )
