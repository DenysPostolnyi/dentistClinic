"""
Functions for testing api
"""
import requests

def create_doctor():
    # creating doctor
    response_all_doctors = requests.get("http://127.0.0.1:5000/doctor-api",
                                        timeout=1000)
    if isinstance(response_all_doctors.json(), dict) and "message" in response_all_doctors.json().keys():
        amount_before = 0
    else:
        amount_before = len(response_all_doctors.json())

    var = amount_before + 1
    doctor_attrs = {
        "full_name": f"Test Doctor{var}",
        "seniority": 3,
        "specialty": "ORTHOPEDIST",
        "phone_number": f"09377817{var}",
        "email": f"testemail{var}@gmail.com"
    }
    return requests.post("http://127.0.0.1:5000/doctor-api", json=doctor_attrs,
                         timeout=1000)


def create_patient():
    response_all_patients = requests.get("http://127.0.0.1:5000/patient-api",
                                         timeout=1000)
    if isinstance(response_all_patients.json(), dict) and "message" in response_all_patients.json().keys():
        amount_before = 0
    else:
        amount_before = len(response_all_patients.json())

    var = amount_before + 1
    patient_attrs = {
        "full_name": f"Test Patient{var}",
        "year_of_birth": 2000,
        "kind_of_ache": "MILD",
        "phone_number": f"09377817{var}",
        "email": f"testemail{var}@gmail.com"
    }
    return requests.post("http://127.0.0.1:5000/patient-api", json=patient_attrs,
                         timeout=1000)


def delete_doctor(doctor_id):
    requests.delete(
        f"http://127.0.0.1:5000/doctor-api/{doctor_id}",
        timeout=1000)


def delete_patient(patient_id):
    requests.delete(
        f"http://127.0.0.1:5000/patient-api/{patient_id}",
        timeout=1000)
