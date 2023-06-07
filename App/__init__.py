from flask import Flask
from flask_restful import Api, Resource
from flask_wtf import CSRFProtect


app = Flask(__name__)
api = Api(app)
csrf = CSRFProtect()


def start_app():
    # applicatio config
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "katakakekukukukakikakakukakukenapaku6969"

    # cross site request forgery protection
    csrf.init_app(app)

    # blueprints import
    from .public_views import public_views

    # blueprints declaration
    app.register_blueprint(public_views, url_prefix="/")

    return app
