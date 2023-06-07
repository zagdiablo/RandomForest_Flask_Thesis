from flask import Blueprint, render_template, redirect, request


public_views = Blueprint("public_views", __name__)


@public_views.route("/", methods=["GET"])
def init():
    return redirect("/home")


@public_views.route("/home", methods=["GET"])
def home_page():
    return render_template("public/home.html")
