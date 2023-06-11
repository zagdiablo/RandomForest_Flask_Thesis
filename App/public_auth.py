from flask import Blueprint, render_template, flash, redirect, request
from flask_login import login_user, logout_user
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
    return render_template("public/login.html")


@public_auth.route("/user_login", methods=["POST"])
def handle_login():
    email = request.form.get("email")
    password = request.form.get("password")

    to_login_user = request.query.filter_by(email=email).first()

    if to_login_user:
        if check_password_hash(to_login_user.password, password):
            login_user(to_login_user)
            return redirect("/profile")

    return redirect("/login")


#
#
# API untuk handle halaman register
@public_auth.route("/register", methods=["GET"])
def register_page():
    return render_template("public/register.html")


@public_auth.route("/user_register", methods=["POST"])
def handle_register():
    nama_lengkap = request.form.get("nama_lengkap")
    email = request.form.get("email")
    password = request.form.get("password")

    check_user = User.query.filter_by(email=email).first()
    if not check_user:
        new_user = User(
            nama_lengkap=nama_lengkap,
            email=email,
            password=generate_password_hash(password, "sha256"),
        )
        db.session.add(new_user)
        db.session.commit()

        flash(f"Akun berhasil dibuat, silahkan login", category="success")
        return redirect("/login")

    flash(f"Email telah dipakai")
    return redirect("/register")
