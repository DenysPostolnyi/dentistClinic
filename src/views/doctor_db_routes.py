from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from src.models.models import *
from src.service import doctor_service

doctor_db_routes = Blueprint('doctor_db_routes', __name__,
                             template_folder='templates')


@doctor_db_routes.route('/doctor-add')
def adding():
    try:
        doctor = Doctor(full_name="Derek", seniority=4, specialty=Specialty.THERAPIST, phone_number="0636582647",
                        email="email2@gmail.com")
        doctor_service.add_doctors(doctor)
        return render_template(f'good.html')
    except TemplateNotFound:
        abort(404)


@doctor_db_routes.route('/doctor-get')
def get_all():
    try:
        print(doctor_service.get_all())
        print("<---------------->")
        print(doctor_service.get_one_by_id("1"))
        return render_template(f'good.html')
    except TemplateNotFound:
        abort(404)


@doctor_db_routes.route('/doctor-update')
def edit():
    try:
        doctor = Doctor(full_name="Chak", seniority=2, specialty=Specialty.ORTHOPEDIST, phone_number="0682748592",
                        email="email@gmail.com")
        doctor_service.update(1, doctor)
        return render_template(f'good.html')
    except TemplateNotFound:
        abort(404)


@doctor_db_routes.route('/doctor-delete')
def delete():
    try:
        doctor_service.delete(1)
        return render_template(f'good.html')
    except TemplateNotFound:
        abort(404)
