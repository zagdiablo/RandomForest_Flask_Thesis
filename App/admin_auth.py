from flask import Blueprint, render_template, redirect, flash, request, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


from .models import User


admin_auth = Blueprint("admin_auth", __name__)


#
#
# API untuk handle admin login
# cek user adalah admin atau tidak, jika user bukan admin
# maka tidak dapat mengakses halaman login admin
@admin_auth.route("/admin_login", methods=["GET"])
def admin_login_page():
    user_check = User.query.get(current_user.get_id())
    if user_check:
        if not user_check.is_admin:
            return redirect(url_for("public_views_loggedin.profile_page"))

    if current_user.is_authenticated:
        return redirect(url_for("admin_views.admin_dashboard"))

    return render_template("admin/auth-login.html")


# handle login request dari halaman login
@admin_auth.route("/handle_admin_login", methods=["POST"])
def handle_admin_login():
    email = request.form.get("email")
    password = request.form.get("password")

    check_admin = User.query.filter_by(email=email).first()

    if check_admin:
        if check_password_hash(check_admin.password, password) and check_admin.is_admin:
            login_user(check_admin)
            return redirect(url_for("admin_views.admin_dashboard"))

    flash("Email atau password salah", category="error")
    return redirect("admin_login")


#
#
# API untuk handle admin logout
@admin_auth.route("/admin_logout", methods=["GET"])
@login_required
def admin_logout():
    check_user = User.query.get(current_user.get_id())
    if not check_user.is_admin:
        return redirect(url_for("public_views_loggedin.profile_page"))

    logout_user()
    return redirect("/admin_login")
