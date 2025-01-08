import uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import StoreModel

from .schemas import StoreSchema, GeneralResponseSchema


blp = Blueprint("homepage", __name__, description="The homepage of the API")


@blp.route("/")
class Homepage(MethodView):
    def get(self):
        """The homepage of the API"""
        return """
        <html>
            <head>
            <title>Homepage</title>
            </head>
            <body>
            <h1>Welcome to the API</h1>
            <p><a href="/docs">Go to API Documentation</a></p>
            </body>
        </html>
        """

    @blp.route("/status")
    class Status(MethodView):
        def get(self):
            """Check the status of the API"""
            return {"status": "API is running"}
