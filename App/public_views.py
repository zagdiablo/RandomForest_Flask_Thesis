from flask import Blueprint, render_template, redirect, request, flash
from flask_login import current_user

from .models import User, Rumah, Agen, Kecamatan
from . import db


public_views = Blueprint("public_views", __name__)


#
#
# API untuk handle halaman home
@public_views.route("/", methods=["GET"])
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

    all_kecamatan = Kecamatan.query.all()

    return render_template(
        "public/cari_rumah.html",
        user_is_authenticated=user_is_authenticated,
        all_kecamatan=all_kecamatan,
    )


@public_views.route("/handle_cari_rumah", methods=["POST"])
def handle_cari_rumah():
    user_is_authenticated = current_user.is_authenticated

    all_rumah = Rumah.query.all()
    all_kecamatan = Kecamatan.query.all()

    kecamatan = request.form.get("search_bar_by_kecamatan")
    dropdown_lantai = request.form.get("dropdown_lantai")
    dropdown_luas = request.form.get("dropdown_luas")
    dropdown_kamar_tidur = request.form.get("dropdown_kamar_tidur")
    dropdown_kamar_mandi = request.form.get("dropdown_kamar_mandi")
    dropdown_harga = request.form.get("dropdown_harga")
    checbox_gym = request.form.get("checkbox_gym")
    checkbox_masjid = request.form.get("checkbox_masjid")
    checkbox_taman = request.form.get("checkbox_taman")
    checkbox_playground = request.form.get("checkbox_playground")
    checkbox_kolam_renang = request.form.get("checkbox_kolam_renang")

    # TODO pengolahan data dan rekomendation system
    # TODO flask query builder
    query_rumah = Rumah.query.filter(Rumah.kecamatan == kecamatan)

    return render_template(
        "public/cari_rumah.html",
        user_is_authenticated=user_is_authenticated,
        all_rumah=all_rumah,
        all_kecamatan=all_kecamatan,
        kecamatan_query=kecamatan,
        query_rumah=query_rumah,
    )


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
# API untuk handle detail rumah
@public_views.route("/detail_rumah", methods=["GET"])
def detail_rumah():
    return render_template("public/detail-rumah.html")


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
