"""
Routes for testing DB services
"""
import requests
from flask import Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound

doctor_routes = Blueprint('doctor_routes', __name__,
                          template_folder='templates')


@doctor_routes.route('/doctors')
def doctor_index():
    try:
        doctors = requests.get("http://127.0.0.1:5000/doctor-api").json()
        if isinstance(doctors, list):
            return render_template('doctor/doctors.html', doctors=[
                {"doctor_id": doctor['doctor_id'], "full_name": doctor['full_name'],
                 "specialty": doctor['specialty']} for doctor in doctors
            ])
        else:
            return render_template('doctor/doctors.html', doctors=[])
    except TemplateNotFound:
        abort(404)


@doctor_routes.route("/doctors/delete/<int:doctor_id>")
def delete(doctor_id):
    request = requests.delete(f"http://127.0.0.1:5000/doctor-api/{doctor_id}")
    return redirect(url_for('doctor_routes.doctor_index'))


@doctor_routes.route("/doctors/<int:doctor_id>")
def info(doctor_id):
    request = requests.get(f"http://127.0.0.1:5000/doctor-api/{doctor_id}")
    if request.status_code == 200:
        doctor = request.json()
        doctor['specialty'] = doctor['specialty']
        return render_template("doctor/doctorInfo.html", doctor = doctor)
    return redirect(url_for('doctor_routes.doctor_index'))
