from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db

#####
# file ini menghandle otentikasi user untuk login dan register
# lalu dialihkan ke API yang ada pada public_views_authenticated.py
#####

public_auth = Blueprint("public_auth", __name__)


#
#
# API untuk handle halaman login
@public_auth.route("/login", methods=["GET"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("public_views_loggedin.profile_page"))
    return render_template("public/login_register.html")


@public_auth.route("/handle_login", methods=["POST"])
def handle_login():
    email = request.form.get("email")
    password = request.form.get("password")

    to_login_user = User.query.filter_by(email=email).first()

    if to_login_user:
        if check_password_hash(to_login_user.password, password):
            login_user(to_login_user)
            flash(f"Selamat datang!", category="success")
            return redirect(url_for("public_views_loggedin.profile_page"))

    flash(f"email atau password salah", category="error")
    return redirect("/login")


#
#
# API untuk handle logout
@public_auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


#
#
# API untuk handle halaman register
@public_auth.route("/register", methods=["GET"])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("public_views_loggedin.profile_page"))
    return render_template("public/login_register.html")


@public_auth.route("/handle_register", methods=["POST"])
def handle_register():
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")

    check_user = User.query.filter_by(email=email).first()
    if password == confirm_password:
        if not check_user:
            new_user = User(
                email=email,
                password=generate_password_hash(password, "sha256"),
                is_admin=False,
            )
            db.session.add(new_user)
            db.session.commit()

            flash(f"Akun berhasil dibuat, silahkan login", category="success")
            return redirect("/login")
        else:
            flash(f"Email telah dipakai", category="error")
    else:
        flash(f"Password tidak sesuai", category="error")

    return redirect("/register")
