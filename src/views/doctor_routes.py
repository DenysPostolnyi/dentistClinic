"""
Routes for testing DB services
"""
import requests
from flask import Blueprint, render_template, abort, redirect, url_for, request
from jinja2 import TemplateNotFound

doctor_routes = Blueprint('doctor_routes', __name__,
                          template_folder='templates')


@doctor_routes.route('/doctors', methods=['GET'])
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


@doctor_routes.route("/doctors/delete/<int:doctor_id>", methods=['GET'])
def delete(doctor_id):
    try:
        request = requests.delete(f"http://127.0.0.1:5000/doctor-api/{doctor_id}")
        return redirect(url_for('doctor_routes.doctor_index'))
    except TemplateNotFound:
        abort(404)


@doctor_routes.route("/doctors/<int:doctor_id>", methods=['GET'])
def info(doctor_id):
    try:
        request = requests.get(f"http://127.0.0.1:5000/doctor-api/{doctor_id}")
        if request.status_code == 200:
            doctor = request.json()
            return render_template("doctor/doctorInfo.html", doctor=doctor)
        return redirect(url_for('doctor_routes.doctor_index'))
    except TemplateNotFound:
        abort(404)


@doctor_routes.route("/doctors/add", methods=['GET', 'POST'])
def add():
    try:
        if request.method == 'GET':
            return render_template("doctor/doctorAdd.html")
        new_doctor = request.form
        req = requests.post("http://127.0.0.1:5000/doctor-api", json=new_doctor)
        if req.status_code == 200:
            return redirect(url_for('doctor_routes.info', doctor_id=req.json()['doctor']['doctor_id']))
        else:
            return redirect(url_for('doctor_routes.doctor_index'))
    except TemplateNotFound:
        abort(404)


@doctor_routes.route("/doctors-edit/<int:doctor_id>", methods=['GET', 'POST'])
def edit(doctor_id):
    try:
        doctor_from_db = requests.get(f"http://127.0.0.1:5000/doctor-api/{doctor_id}")
        if doctor_from_db.status_code == 200:
            if request.method == 'GET':
                return render_template("doctor/doctorsEdit.html", doctor=doctor_from_db.json())
            new_doctor = request.form
            req = requests.put(f"http://127.0.0.1:5000/doctor-api/{doctor_id}", json=new_doctor).json()
            return redirect(url_for('doctor_routes.info', doctor_id=req['doctor_id']))
        return redirect(url_for('doctor_routes.doctor_index'))
    except TemplateNotFound:
        abort(404)
