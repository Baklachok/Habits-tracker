from flask import Flask
from flasgger import Swagger
import os

from app.extentions import db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.environ.get('MYSQL_USER')}:{os.environ.get('MYSQL_PASSWORD')}@{os.environ.get('MYSQL_HOST')}:{os.environ.get('MYSQL_PORT')}/{os.environ.get('MYSQL_DATABASE')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Swagger
    app.config["SWAGGER"] = {"title": "Flask MySQL API", "uiversion": 3}
    swagger = Swagger(app)

    db.init_app(app)

    from .models import User
    from .routes import user_bp

    app.register_blueprint(user_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app
