from flask import Blueprint, render_template, redirect, flash


from .models import User


admin_auth = Blueprint("admin_auth", __name__)


@admin_auth.route("/admin_login", methods=["GET"])
def admin_login_page():
    return render_template("admin/auth-login.html")


@admin_auth.route("/handle_admin_login", methods=["POST"])
def handle_admin_login():
    check_admin = User.query.get(1)

    flash("Email atau password salah")
    return redirect("admin_login")
