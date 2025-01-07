from celery import Celery
from flask import Flask
import os
from dotenv import load_dotenv


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["RESULT_BACKEND_CELERY"],
        broker=app.config["CELERY_BROKER_URL"],
        include=["tasks"],  # Include the tasks module
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


load_dotenv()
flask_app = Flask(__name__)
flask_app.config["CELERY_BROKER_URL"] = os.getenv(
    "CELERY_BROKER_URL", "redis://localhost:6379"
)
flask_app.config["RESULT_BACKEND_CELERY"] = os.getenv(
    "RESULT_BACKEND_CELERY", "redis://localhost:6379"
)
celery = make_celery(flask_app)
