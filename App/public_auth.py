from flask import Blueprint, render_template, redirect, request

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
    return redirect("/login")


#
#
# API untuk handle halaman register
@public_auth.route("/register", methods=["GET"])
def register_page():
    return render_template("public/register.html")


@public_auth.route("/user_register", methods=["POST"])
def handle_register():
    return redirect("/register")
