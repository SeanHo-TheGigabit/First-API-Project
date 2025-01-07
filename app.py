import os

from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate

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

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TaskBlueprint)

    celery = make_celery(app)

    return app
