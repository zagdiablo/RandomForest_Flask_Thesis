from flask import Blueprint, render_template, redirect, request
from flask_login import login_required


#####
# file ini menghandle tampilan halaman yang tidak membutuhkan user login
#####


public_views = Blueprint("public_views", __name__)


#
#
# API untuk handle inisialisasi keperluan webapp
@public_views.route("/", methods=["GET"])
def init():
    return redirect("/home")


#
#
# API untuk handle halaman home
@public_views.route("/home", methods=["GET"])
def home_page():
    return render_template("public/home.html")


#
#
# API untuk handle halaman pencarian rumah
@public_views.route("/cari_rumah", methods=["GET"])
def cari_rumah_page():
    return render_template("public/cari_rumah.html")


@public_views.route("/get_price_suggestion", methods=["POST"])
def get_price_suggestion():
    #####
    # TODO handle logika machine learning & query data hasil
    # TODO requirement: untuk user yang belum login reange parameter gaji di tiadakan
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
    return render_template("public/about.html")


#
#
# API untuk handle halaman kontak
@public_views.route("/contact", methods=["GET"])
def contact_page():
    return render_template("public/contact.html")
