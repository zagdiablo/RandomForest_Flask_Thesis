from flask import Blueprint, render_template


admin_views = Blueprint("admin_views", __name__)


@admin_views.route("/dashboard", methods=["GET"])
def dashboard_page():
    return render_template("<h1>Hello World</h1>")
