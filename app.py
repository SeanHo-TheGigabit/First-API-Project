import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv
from db import db

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.user import blp as UserBlueprint
from resources.task import blp as TaskBlueprint

from celery_config import make_celery


def create_app(db_url=None):
    """Create a Flask application

    With the app factory pattern, we write a function that returns app. That way we can pass configuration values to the function, so that we configure the app before getting it back.
    This is especially useful for testing, but also if you want to do things like have staging and production apps.
    """
    app = Flask(__name__)
    load_dotenv()
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CELERY_BROKER_URL"] = os.getenv(
        "CELERY_BROKER_URL", "redis://localhost:6379"
    )
    app.config["RESULT_BACKEND_CELERY"] = os.getenv(
        "RESULT_BACKEND_CELERY", "redis://localhost:6379"
    )
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", None)
    if app.config["JWT_SECRET_KEY"] is None:
        raise ValueError("No JWT secret key set")
    jwt = JWTManager(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TaskBlueprint)

    celery = make_celery(app)

    ## JWT error handling
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    return app
