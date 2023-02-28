"""
Routes for testing DB services
"""
import requests
from flask import Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound

patient_routes = Blueprint('patient_routes', __name__,
                           template_folder='templates')


@patient_routes.route('/patients')
def patient_index():
    try:
        patients = requests.get("http://127.0.0.1:5000/patient-api").json()
        if isinstance(patients, list):
            return render_template('patient/patients.html', patients=[
                {"patient_id": patient['patient_id'], "full_name": patient['full_name'],
                 "year_of_birth": patient['year_of_birth']} for patient in patients
            ])
        else:
            return render_template('patient/patients.html', patients=[])
    except TemplateNotFound:
        abort(404)


@patient_routes.route("/patients/delete/<int:patient_id>")
def delete_patient(patient_id):
    request = requests.delete(f"http://127.0.0.1:5000/patient-api/{patient_id}")
    return redirect(url_for('patient_routes.patient_index'))
