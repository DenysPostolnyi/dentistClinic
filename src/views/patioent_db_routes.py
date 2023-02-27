"""
Routes for testing DB services
"""
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from src.models.models import Patient, KindOfAche
from src.service import patient_service

patient_db_routes = Blueprint('patient_db_routes', __name__,
                              template_folder='templates')


@patient_db_routes.route('/patient-add')
def adding():
    """
    Rout which call service for adding patient to DB
    :return: if service was called without errors, return page "Good"
    else returns error
    """
    try:
        patient = Patient(full_name="Derek", year_of_birth=2000, kind_of_ache=KindOfAche.MILD,
                          phone_number="0682748592",
                          email="email@gmail.com")
        patient_service.add_patient(patient)
        return render_template('good.html')
    except TemplateNotFound:
        abort(404)


@patient_db_routes.route('/patient-get')
def get_all():
    """
    Rout which call service for getting all patients and by id from DB
    :return: if service was called without errors, return page "Good"
    else returns error
    """
    try:
        print(patient_service.get_all())
        print("<---------------->")
        print(patient_service.get_one_by_id("1"))
        return render_template('good.html')
    except TemplateNotFound:
        abort(404)


@patient_db_routes.route('/patient-update')
def edit():
    """
    Rout which call service for edit patient in DB
    :return: if service was called without errors, return page "Good"
    else returns error
    """
    try:
        patient = Patient(full_name="Chak", year_of_birth=2002, kind_of_ache=KindOfAche.MILD,
                          phone_number="0682748592",
                          email="email@gmail.com")
        patient_service.update(1, patient)
        return render_template('good.html')
    except TemplateNotFound:
        abort(404)


@patient_db_routes.route('/patient-delete')
def delete():
    """
    Rout which call service for delete patient from DB
    :return: if service was called without errors, return page "Good"
    else returns error
    """
    try:
        patient_service.delete(1)
        return render_template('good.html')
    except TemplateNotFound:
        abort(404)
