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
    """
    Rout for page with list of doctors
    :return:
    """
    try:
        doctors = requests.get("http://127.0.0.1:5000/doctor-api", timeout=1000).json()
        if isinstance(doctors, list):
            amount = requests.get("http://127.0.0.1:5000/doctor-api/count", timeout=1000).json()['amount']
            return render_template('doctor/doctors.html', doctors=[
                {"doctor_id": doctor['doctor_id'], "full_name": doctor['full_name'],
                 "specialty": doctor['specialty']} for doctor in doctors
            ], amount=amount)
        return render_template('doctor/doctors.html', doctors=[])
    except TemplateNotFound:
        abort(404)


@doctor_routes.route("/doctors/delete/<int:doctor_id>", methods=['GET'])
def delete(doctor_id):
    """
    Rout for delete doctor
    :param doctor_id:
    :return:
    """
    try:
        requests.delete(f"http://127.0.0.1:5000/doctor-api/{doctor_id}", timeout=1000)
        return redirect(url_for('doctor_routes.doctor_index'))
    except TemplateNotFound:
        abort(404)


@doctor_routes.route("/doctors/<int:doctor_id>", methods=['GET', 'POST'])
def info(doctor_id):
    """
    Rout for page with info about doctor
    :param doctor_id:
    :return:
    """
    try:
        req = requests.get(f"http://127.0.0.1:5000/doctor-api/{doctor_id}", timeout=1000)
        if req.status_code == 200:
            if request.method == "GET":
                take_patients = requests.get(f"http://127.0.0.1:5000/doctor-api/clients/{doctor_id}", timeout=1000)
                if take_patients.status_code == 200:
                    doctor = req.json()
                    patients = take_patients.json()
                    return render_template("doctor/doctorInfo.html", doctor=doctor, patients=patients)

            date_from = request.form['date_from']
            date_to = request.form['date_to']
            date = {
                "date_from": date_from,
                "date_to": date_to,
            }

            take_patients = requests.post(f"http://127.0.0.1:5000/doctor-api/clients/{doctor_id}", json=date,
                                          timeout=1000)
            if take_patients.status_code == 200:
                doctor = req.json()
                patients = take_patients.json()
                return render_template("doctor/doctorInfo.html", doctor=doctor, patients=patients)
        return redirect(url_for('doctor_routes.doctor_index'))
    except TemplateNotFound:
        abort(404)


@doctor_routes.route("/doctors/add", methods=['GET', 'POST'])
def add():
    """
    Rout for page for adding new doctor
    :return:
    """
    try:
        if request.method == 'GET':
            return render_template("doctor/doctorAdd.html")
        new_doctor = request.form
        req = requests.post("http://127.0.0.1:5000/doctor-api", json=new_doctor, timeout=1000)
        if req.status_code == 200:
            return redirect(url_for('doctor_routes.info', doctor_id=req.json()['doctor']['doctor_id']))
        return redirect(url_for('doctor_routes.doctor_index'))
    except TemplateNotFound:
        abort(404)


@doctor_routes.route("/doctors-edit/<int:doctor_id>", methods=['GET', 'POST'])
def edit(doctor_id):
    """
    Rout for page for editing info about doctor
    :param doctor_id:
    :return:
    """
    try:
        doctor_from_db = requests.get(f"http://127.0.0.1:5000/doctor-api/{doctor_id}", timeout=1000)
        if doctor_from_db.status_code == 200:
            if request.method == 'GET':
                return render_template("doctor/doctorsEdit.html", doctor=doctor_from_db.json())
            new_doctor = request.form
            req = requests.put(f"http://127.0.0.1:5000/doctor-api/{doctor_id}", json=new_doctor, timeout=1000).json()
            return redirect(url_for('doctor_routes.info', doctor_id=req['doctor_id']))
        return redirect(url_for('doctor_routes.doctor_index'))
    except TemplateNotFound:
        abort(404)
