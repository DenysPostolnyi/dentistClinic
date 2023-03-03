"""
Routes for testing DB services
"""
import requests
from flask import Blueprint, render_template, abort, redirect, url_for, request
from jinja2 import TemplateNotFound

patient_routes = Blueprint('patient_routes', __name__,
                           template_folder='templates')


@patient_routes.route('/patients')
def patient_index():
    """
    Rout for page with list of patients
    :return:
    """
    try:
        patients = requests.get("http://127.0.0.1:5000/patient-api", timeout=1000).json()
        if isinstance(patients, list):
            return render_template('patient/patients.html', patients=[
                {"patient_id": patient['patient_id'], "full_name": patient['full_name'],
                 "year_of_birth": patient['year_of_birth']} for patient in patients
            ])
        return render_template('patient/patients.html', patients=[])
    except TemplateNotFound:
        abort(404)


@patient_routes.route("/patients/delete/<int:patient_id>")
def delete_patient(patient_id):
    """
    Rout for delete patient
    :param patient_id:
    :return:
    """
    requests.delete(f"http://127.0.0.1:5000/patient-api/{patient_id}", timeout=1000)
    return redirect(url_for('patient_routes.patient_index'))


@patient_routes.route("/patients/<int:patient_id>")
def info(patient_id):
    """
    Rout for page with info about patient
    :param patient_id:
    :return:
    """
    req = requests.get(f"http://127.0.0.1:5000/patient-api/{patient_id}", timeout=1000)
    if req.status_code == 200:
        patient = req.json()
        if patient['doctor_id']:
            doctor = requests.get(f"http://127.0.0.1:5000/doctor-api/{patient['doctor_id']}", timeout=1000)
            if doctor.status_code == 200:
                return render_template("patient/patientInfo.html", patient=patient, appointed_doctor=doctor.json())
            patient['doctor_id'] = None

        take_doctors = requests.get("http://127.0.0.1:5000/doctor-api", timeout=1000)
        all_doctors = None
        if take_doctors.status_code == 200:
            all_doctors = take_doctors.json()
        return render_template("patient/patientInfo.html", patient=patient, doctors=all_doctors)
    return redirect(url_for('patient_routes.patient_index'))


@patient_routes.route("/patients/add", methods=['GET', 'POST'])
def add():
    """
    Rout for page for adding new patient
    :return:
    """
    try:
        if request.method == 'GET':
            return render_template("patient/patientAdd.html")
        new_patient = request.form
        req = requests.post("http://127.0.0.1:5000/patient-api", json=new_patient, timeout=1000)
        if req.status_code == 200:
            return redirect(url_for('patient_routes.info', patient_id=req.json()['patient']['patient_id']))
        return redirect(url_for('patient_routes.patient_index'))
    except TemplateNotFound:
        abort(404)


@patient_routes.route("/patients-edit/<int:patient_id>", methods=['GET', 'POST'])
def edit(patient_id):
    """
    Rout for page for editing patient
    :param patient_id:
    :return:
    """
    try:
        patient_from_db = requests.get(f"http://127.0.0.1:5000/patient-api/{patient_id}", timeout=1000)
        if patient_from_db.status_code == 200:
            if request.method == 'GET':
                return render_template("patient/patientEdit.html", patient=patient_from_db.json())
            new_patient = request.form
            req = requests.put(f"http://127.0.0.1:5000/patient-api/{patient_id}", json=new_patient, timeout=1000).json()
            return redirect(url_for('patient_routes.info', patient_id=req['patient_id']))
        return redirect(url_for('patient_routes.patient_index'))
    except TemplateNotFound:
        abort(404)


@patient_routes.route("/patients-appoint/<int:patient_id>", methods=['POST'])
def appointment(patient_id):
    """
    Rout for make appoint
    :param patient_id:
    :return:
    """
    try:
        date_from_form = request.form['date_of_appointment']
        doctor_id = request.form['doctor_id']
        data = {
            'doctor_id': int(doctor_id),
            'date_of_appointment': date_from_form
        }
        appoint = requests.post(f"http://127.0.0.1:5000/patient-api/appoint/{patient_id}", json=data, timeout=1000)
        if appoint.status_code == 200:
            return redirect(url_for('patient_routes.info', patient_id=patient_id))
        return redirect(url_for('patient_routes.patient_index'))
    except TemplateNotFound:
        abort(404)


@patient_routes.route("/patients-unappoint/<int:patient_id>")
def cancel_appointment(patient_id):
    """
    Rout for cancel appoint
    :param patient_id:
    :return:
    """
    try:
        unappoint = requests.delete(f"http://127.0.0.1:5000/patient-api/appoint/{patient_id}", timeout=1000)
        if unappoint.status_code == 200:
            return redirect(url_for('patient_routes.info', patient_id=patient_id))
        return redirect(url_for('patient_routes.patient_index'))
    except TemplateNotFound:
        abort(404)
