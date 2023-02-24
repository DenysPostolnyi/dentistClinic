"""
Init file for app
"""
from flask import Flask
from src.config import DBSettings


def create_app(test_config=None):
    """
    creating app
    :param test_config:
    :return: app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = DBSettings.SQLALCHEMY_DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from src.models.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    from src.models.models import Doctor, Patient
    #
    # from src.views import doctor_db_routes, patioent_db_routes
    # app.register_blueprint(doctor_db_routes.doctor_db_routes)
    # app.register_blueprint(patioent_db_routes.patient_db_routes)

    return app
