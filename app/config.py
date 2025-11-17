import os

from flask import Flask


def configure_base(app: Flask):
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

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(
        os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_SECONDS", 900)
    )


def configure_database(app: Flask, testing: bool):
    if testing:
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            SQLALCHEMY_ENGINE_OPTIONS={"connect_args": {"check_same_thread": False}},
            JWT_SECRET_KEY="test-secret-key",
        )
        app.logger.info("Configured for TESTING")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"mysql+pymysql://{os.environ.get('MYSQL_USER')}:"
            f"{os.environ.get('MYSQL_PASSWORD')}@"
            f"{os.environ.get('MYSQL_HOST')}:"
            f"{os.environ.get('MYSQL_PORT')}/"
            f"{os.environ.get('MYSQL_DATABASE')}"
        )
        app.logger.info("Configured for PROD/DEV MySQL")
