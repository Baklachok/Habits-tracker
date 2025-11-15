from flask import Flask
import os

from flask_smorest import Api


from app.extentions import db, jwt, migrate


def create_app():
    from dotenv import load_dotenv

    load_dotenv()

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.environ.get('MYSQL_USER')}:{os.environ.get('MYSQL_PASSWORD')}@{os.environ.get('MYSQL_HOST')}:{os.environ.get('MYSQL_PORT')}/{os.environ.get('MYSQL_DATABASE')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT конфиг
    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY", "dev-secret"
    )  # в проде — сильный секрет
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(
        os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_SECONDS", 900)
    )

    # API Docs — smorest
    app.config["API_TITLE"] = "Flask MySQL API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    app.config["API_SPEC_OPTIONS"] = {
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
        "security": [{"BearerAuth": []}],
    }

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    api = Api(app)

    from .blueprints.auth import auth_blp
    from .blueprints.habits import habit_blp
    from .blueprints.users import user_blp
    from .blueprints.habit_log import habit_log_blp

    # register blueprints
    api.register_blueprint(auth_blp)
    api.register_blueprint(user_blp)
    api.register_blueprint(habit_blp, url_prefix="/habits")
    api.register_blueprint(habit_log_blp)

    return app
