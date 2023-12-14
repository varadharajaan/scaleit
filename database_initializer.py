from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from autoscaler import app

db = SQLAlchemy(app)


class DatabaseInitializer:

    @app.before_request
    def create_tables(self):
        db.create_all()
