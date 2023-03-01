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


@patient_routes.route("/patients/<int:patient_id>")
def info(patient_id):
    req = requests.get(f"http://127.0.0.1:5000/patient-api/{patient_id}")
    if req.status_code == 200:
        print("<===============+++>")
        # print(url_for(request.endpoint, patient_id=request.args.get('patient_id')))

        print("<===============+++>")
        patient = req.json()
        patient['kind_of_ache'] = patient['kind_of_ache']
        return render_template("patient/patientInfo.html", patient=patient)
    return redirect(url_for('patient_routes.patient_index'))


@patient_routes.route("/patients/add", methods=['GET', 'POST'])
def add():
    try:
        if request.method == 'GET':
            return render_template("patient/patientAdd.html")
        new_patient = request.form
        req = requests.post("http://127.0.0.1:5000/patient-api", json=new_patient)
        if req.status_code == 200:
            return redirect(url_for('patient_routes.info', patient_id=req.json()['patient']['patient_id']))
        return redirect(url_for('patient_routes.patient_index'))
    except TemplateNotFound:
        abort(404)
