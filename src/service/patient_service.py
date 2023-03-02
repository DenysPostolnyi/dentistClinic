"""
Patient services for working with DB
"""
from src.models.models import db, Patient, Doctor
from src.service import doctor_service


def add_patient(patient):
    """
    Function for adding patient to DB
    :param patient:
    """
    db.session.add(patient)
    db.session.commit()
    all = get_all()
    return all[len(all) - 1]


def get_all():
    """
    Function for getting all patients from DB
    :return list of Patient objects:
    """
    return Patient.query.all()


def get_one_by_id(patient_id):
    """
    Function for getting patient from DB by id
    :param patient_id:
    :return patient:
    """
    patient = Patient.query.get(patient_id)
    if patient:
        return patient
    raise RuntimeError(f"Patient with id: {patient_id} was not found")


def update(patient_id, patient):
    """
    Function for updating patient in DB
    :param patient_id:
    :param patient:
    """
    patient_for_edit = Patient.query.get(patient_id)
    if patient_for_edit:
        patient_for_edit.full_name = patient.full_name
        patient_for_edit.year_of_birth = patient.year_of_birth
        patient_for_edit.kind_of_ache = patient.kind_of_ache
        patient_for_edit.phone_number = patient.phone_number
        patient_for_edit.email = patient.email

        db.session.add(patient_for_edit)
        db.session.commit()
    else:
        raise RuntimeError(f"Patient with id: {patient_id} was not found")


def delete(patient_id):
    """
    Function for deleting patient from DB
    :param patient_id:
    """
    patient = Patient.query.get(patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
    else:
        raise RuntimeError(f"Patient with id: {patient_id} was not found")


def make_appointment(patient_id, data):
    patient_for_appoint = Patient.query.get(patient_id)
    if patient_for_appoint:
        try:
            doctor_service.get_one_by_id(int(data['doctor_id']))
            patient_for_appoint.doctor_id = int(data['doctor_id'])
            patient_for_appoint.date_of_appointment = data['date_of_appointment']
            db.session.add(patient_for_appoint)
            db.session.commit()
            return patient_for_appoint
        except RuntimeError as error:
            raise error
    raise RuntimeError(f"Patient with id: {patient_id} was not found")
