from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user


from .models import User


admin_views = Blueprint("admin_views", __name__)


######################################
# functions
######################################


def check_admin():
    user_object = User.query.get(current_user.get_id())
    return user_object.is_admin


######################################


#
#
# API untuk handle admin dashboard
@admin_views.route("/admin_dashboard", methods=["GET"])
@login_required
def admin_dashboard():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    admin_user = User.query.get(current_user.get_id())
    return render_template("admin/dashboard.html", admin_user=admin_user)


#
#
# API untuk handle admin kecamatan
@admin_views.route("/admin_kecamatan", methods=["GEt"])
@login_required
def admin_kecamatan():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/kecamatan.html")


@admin_views.route("/tambah_kecamatan", methods=["GET"])
@login_required
def tambah_kecamatan():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/tambah-kecamatan.html")


@admin_views.route("/edit_kecamatan", methods=["GET"])
@login_required
def edit_kecamatan():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/edit-kecamatan.html")


@admin_views.route("/handle_tambah_kecamatan", methods=["POST"])
@login_required
def handle_tambah_kecamatan():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return redirect("/tambah_kecamatan")


#
#
# API untuk handle admin rumah
@admin_views.route("/admin_rumah", methods=["GET"])
@login_required
def admin_rumah():
    if not check_admin():
        return redirect(url_for("admin_views_loggedin.profile_page"))

    return render_template("admin/rumah.html")


@admin_views.route("/tambah_rumah", methods=["GET"])
@login_required
def tambah_rumah():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/tambah-rumah.html")


@admin_views.route("/edit_rumah", methods=["GET"])
@login_required
def edit_rumah():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/edit-rumah.html")


#
#
# API untuk handle kontak agen
@admin_views.route("/admin_kontak_agen", methods=["GET"])
@login_required
def admin_kontak_agen():
    if not check_admin():
        return redirect(url_for("admin_views_loggedin.profile_page"))

    return render_template("admin/kontak-agen.html")


@admin_views.route("/tambah_agen", methods=["GET"])
@login_required
def tambah_agen():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/tambah-agen.html")


@admin_views.route("/edit_agen", methods=["GET"])
@login_required
def edit_agen():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/edit-agen.html")


#
#
# API untuk handle admin user
@admin_views.route("/admin_user", methods=["GET"])
@login_required
def admin_user():
    if not check_admin():
        return redirect(url_for("admin_views_loggedin.profile_page"))

    return render_template("admin/user.html")


@admin_views.route("/edit_user", methods=["GET"])
@login_required
def edit_user():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/edit-user.html")
