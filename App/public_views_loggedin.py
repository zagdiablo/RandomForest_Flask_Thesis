from flask import Blueprint, render_template, redirect, request
from flask_login import login_required


public_views_loggedin = Blueprint("public_views_loggedin", __name__)


@public_views_loggedin.route("/profile", methods=["GET"])
@login_required
def profile_page():
    return render_template("public_loggedin/profile.html")
