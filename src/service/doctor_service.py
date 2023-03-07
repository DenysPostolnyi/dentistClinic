"""
Doctor services for working with DB
"""
from src.models.models import db, Doctor, Patient
from src.service import patient_service


# from src.service import patient_service


def add_doctors(doctor):
    """
    Function for adding doctor to DB
    :param doctor:
    """
    db.session.add(doctor)
    db.session.commit()
    all_doctors = get_all()
    return all_doctors[len(all_doctors) - 1]


def get_all():
    """
    Function for getting all doctors from DB
    :return list of Doctor objects:
    """
    return Doctor.query.all()


def count_all():
    """
    Function for counting all doctors
    :return:
    """
    return Doctor.query.count()


def get_one_by_id(doctor_id):
    """
    Function for getting doctor from DB by id
    :param doctor_id:
    :return doctor:
    """
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        return doctor
    raise RuntimeError(f"Doctor with id: {doctor_id} was not found")


def update(doctor_id, doctor):
    """
    Function for updating doctor in DB
    :param doctor_id:
    :param doctor:
    """
    doctor_for_edit = Doctor.query.get(doctor_id)
    if doctor_for_edit:
        doctor_for_edit.full_name = doctor.full_name
        doctor_for_edit.seniority = doctor.seniority
        doctor_for_edit.specialty = doctor.specialty
        doctor_for_edit.phone_number = doctor.phone_number
        doctor_for_edit.email = doctor.email

        db.session.add(doctor_for_edit)
        db.session.commit()
    else:
        raise RuntimeError(f"Doctor with id: {doctor_id} was not found")


def delete(doctor_id):
    """
    Function for deleting doctor from DB
    :param doctor_id:
    """
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        patients = get_list_of_patients(doctor_id)
        for patient in patients:
            patient_service.cancel_appointment(patient.patient_id)
        db.session.delete(doctor)
        db.session.commit()
    else:
        raise RuntimeError(f"Doctor with id: {doctor_id} was not found")


def get_list_of_patients(doctor_id):
    """
    Function for getting all appointed patients to the doctor
    :param doctor_id:
    :return: list of appointed patients
    """
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        result = db.session.query(Patient).join(Doctor).filter(Patient.doctor_id == doctor_id).all()
        return result
    raise RuntimeError(f"Doctor with id: {doctor_id} was not found")


def get_filtered_list_of_patients(doctor_id, date):
    """
    Function for getting appointed patients to the doctor searched by date
    :param doctor_id:
    :param date:
    :return: list of appointed patients
    """
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        result = db.session.query(Patient).join(Doctor).filter(Patient.doctor_id == doctor_id).filter(
            Patient.date_of_appointment >= date['date_from']).filter(
            Patient.date_of_appointment <= date['date_to']).all()
        return result
    raise RuntimeError(f"Doctor with id: {doctor_id} was not found")
