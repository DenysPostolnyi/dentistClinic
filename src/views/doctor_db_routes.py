"""
Routes for testing DB services
"""
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from src.models.models import Doctor, Specialty
from src.service import doctor_service

doctor_db_routes = Blueprint('doctor_db_routes', __name__,
                             template_folder='templates')


@doctor_db_routes.route('/doctor-add')
def adding():
    """
    Rout which call service for adding doctor to DB
    :return: if service was called without errors, return page "Good"
    else returns error
    """
    try:
        doctor = Doctor(full_name="Derek", seniority=4, specialty=Specialty.THERAPIST,
                        phone_number="0636582647", email="email2@gmail.com")
        doctor_service.add_doctors(doctor)
        return render_template(f'good.html')
    except TemplateNotFound:
        abort(404)


@doctor_db_routes.route('/doctor-get')
def get_all():
    """
    Rout which call service for getting all doctors and by id from DB
    :return: if service was called without errors, return page "Good"
    else returns error
    """
    try:
        print(doctor_service.get_all())
        print("<---------------->")
        print(doctor_service.get_one_by_id("1"))
        return render_template(f'good.html')
    except TemplateNotFound:
        abort(404)


@doctor_db_routes.route('/doctor-update')
def edit():
    """
    Rout which call service for edit doctor in DB
    :return: if service was called without errors, return page "Good"
    else returns error
    """
    try:
        doctor = Doctor(full_name="Chak", seniority=2, specialty=Specialty.ORTHOPEDIST, phone_number="0682748592",
                        email="email@gmail.com")
        doctor_service.update(1, doctor)
        return render_template(f'good.html')
    except TemplateNotFound:
        abort(404)


@doctor_db_routes.route('/doctor-delete')
def delete():
    """
    Rout which call service for delete doctor from DB
    :return: if service was called without errors, return page "Good"
    else returns error
    """
    try:
        doctor_service.delete(1)
        return render_template(f'good.html')
    except TemplateNotFound:
        abort(404)
