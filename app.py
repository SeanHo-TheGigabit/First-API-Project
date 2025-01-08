import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv
from db import db
from celery import Celery

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.user import blp as UserBlueprint
from resources.task import blp as TaskBlueprint
from resources.homepage import blp as HomepageBlueprint

from models import TokenBlocklist


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
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["OPENAPI_REDOC_PATH"] = "/redoc"
    app.config["OPENAPI_REDOC_URL"] = (
        "https://rebilly.github.io/ReDoc/releases/latest/redoc.min.js"
    )
    app.config["OPENAPI_RAPIDOC_PATH"] = "/rapidoc"
    app.config["OPENAPI_RAPIDOC_URL"] = (
        "https://cdn.jsdelivr.net/npm/rapidoc/dist/rapidoc-min.js"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CELERY_CONFIG"] = dict(
        broker_url=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379"),
        result_backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379"),
        include=["celery_blueprint.tasks"],
        beat_schedule={
            "task-every-10-seconds": {
                "task": "celery_blueprint.tasks.hello_world",
                "schedule": 10,
            }
        },
    )
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", None)

    if app.config["JWT_SECRET_KEY"] is None:
        raise ValueError("No JWT secret key set")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=5)
    jwt = JWTManager(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TaskBlueprint)
    api.register_blueprint(HomepageBlueprint)

    ## Print all app configurations
    if app.config["DEBUG"]:
        for key, value in app.config.items():
            print(f"{key}: {value}")

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

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    return app


def make_celery(app):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app

    ref: https://github.com/nickjj/build-a-saas-app-with-flask/blob/master/snakeeyes/app.py#L15
    """
    celery = Celery(
        app.import_name,
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.conf.update(app.config.get("CELERY_CONFIG", {}))
    celery.set_default()
    app.extensions["celery"] = celery

    return celery


celery_app = make_celery(create_app())
