"""
Init file for app
"""
import logging

from flask import Flask
from src.models.models import db, migrate
from src.config import DBSettings
from src.rest.doctor_api import api_doctor
from src.rest.patient_api import api_patient

# create a logger instance
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create a file handler that logs messages to a file
file_handler = logging.FileHandler('log/logs.log')
file_handler.setLevel(logging.DEBUG)

# create a console handler that logs messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create a formatter that formats log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add the formatter to the file handler and console handler
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add the file handler and console handler to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = DBSettings.SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)
from src.models.models import Doctor, Patient

app.register_blueprint(api_doctor)
app.register_blueprint(api_patient)
