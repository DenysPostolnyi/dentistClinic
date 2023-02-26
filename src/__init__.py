"""
Init file for app
"""
from flask import Flask
from flask_restful import Api
from src.models.models import db, migrate
from src.config import DBSettings
from src.rest.doctor_api import api_bp

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = DBSettings.SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)
from src.models.models import Doctor, Patient

api = Api()
app.register_blueprint(api_bp)
