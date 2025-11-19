import logging
from flask import Flask, request
from flask_smorest import Api

from app.config import configure_base, configure_database
from app.extentions import db, jwt, migrate


# ============================================================
# ЛОГИРОВАНИЕ
# ============================================================


def setup_logging(app: Flask):
    """Configure logging for the application."""
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    handler = logging.FileHandler("app.log")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)


# ============================================================
# МИДЛВАРЫ
# ============================================================


def setup_middlewares(app: Flask):
    @app.before_request
    def log_request():
        app.logger.info(
            "Request: method=%s, path=%s, args=%s",
            request.method,
            request.path,
            request.args.to_dict(),
        )

    @app.after_request
    def log_response(response):
        app.logger.info(
            "Response: status=%s, length=%s", response.status, response.content_length
        )
        return response


# ============================================================
# APP FACTORY
# ============================================================


def create_app(testing: bool = False):
    from dotenv import load_dotenv

    load_dotenv()

    app = Flask(__name__)

    # Logging
    setup_logging(app)
    app.logger.info("Starting Flask app (testing=%s)", testing)

    # Config
    configure_base(app)
    configure_database(app, testing)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # API + Blueprints
    api = Api(app)

    from .blueprints.auth import auth_blp
    from .blueprints.habits import habit_blp
    from .blueprints.users import user_blp
    from .blueprints.habit_log import habit_log_blp
    from .blueprints.statistics import statistics_blp

    api.register_blueprint(auth_blp)
    api.register_blueprint(user_blp)
    api.register_blueprint(habit_blp, url_prefix="/habits")
    api.register_blueprint(habit_log_blp)
    api.register_blueprint(statistics_blp)

    app.logger.info("Blueprints registered")

    # Middlewares
    setup_middlewares(app)

    return app
