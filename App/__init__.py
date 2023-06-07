from flask import Flask


app = Flask(__name__)


def start_app():
    # applicatio config
    app.config["DEBUG"] = True

    # blueprints import
    from .public_views import public_views

    # blueprints declaration
    app.register_blueprint(public_views, url_prefix="/")

    return app
