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
