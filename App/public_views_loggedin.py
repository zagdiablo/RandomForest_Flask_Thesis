from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user

from .models import User
from . import db


public_views_loggedin = Blueprint("public_views_loggedin", __name__)


#
#
# API untuk menampilkan halaman profile
@public_views_loggedin.route("/profile", methods=["GET"])
@login_required
def profile_page():
    user_profile_data = User.query.get(current_user.get_id())
    user_is_authenticated = current_user.is_authenticated

    return render_template(
        "public_loggedin/profile.html",
        user_profile_data=user_profile_data,
        user_is_authenticated=user_is_authenticated,
    )


# handle pengeditan data user pada halaman profile
# mengambil data dari halama profle menggunakan request
# dan menyimpanya dalam database
@public_views_loggedin.route("/handle_submit_profile", methods=["POST"])
@login_required
def handle_submit_profile():
    nama_lengkap = request.form.get("nama_lengkap")
    email = request.form.get("email")
    alamat_tempat_kerja = request.form.get("alamat_tempat_kerja")
    total_gaji = 0

    gaji_user = request.form.get("gaji_user")
    gaji_pasangan = request.form.get("gaji_pasangan")
    print(gaji_user, gaji_pasangan, "<--- gajinye")

    if gaji_pasangan:
        total_gaji = int(gaji_user) + int(gaji_pasangan)
    elif gaji_user:
        total_gaji = int(gaji_user)
    else:
        total_gaji = int(request.form.get("range_gaji"))

    to_commit_profile = User.query.get(current_user.get_id())
    # TODO front end, jika profil lengkap maka adakan rekomendasi, jika tidak suruh lengkapi
    profile_is_complete = (
        True if nama_lengkap and total_gaji and alamat_tempat_kerja else False
    )

    if to_commit_profile:
        to_commit_profile.nama_lengkap = nama_lengkap
        to_commit_profile.email = email
        to_commit_profile.range_gaji = total_gaji
        to_commit_profile.alamat_tempat_kerja = alamat_tempat_kerja
        to_commit_profile.is_filled = profile_is_complete

    db.session.commit()

    flash(
        "Berhasil mengedit profile",
        category="Success",
    )
    return redirect("/profile")
