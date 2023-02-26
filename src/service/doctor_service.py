"""
Doctor services for working with DB
"""
from src.models.models import db, Doctor


def add_doctors(doctor):
    """
    Function for adding doctor to DB
    :param doctor:
    """
    db.session.add(doctor)
    db.session.commit()


def get_all():
    """
    Function for getting all doctors from DB
    :return list of Doctor objects:
    """
    return Doctor.query.all()


def get_one_by_id(doctor_id):
    """
    Function for getting doctor from DB by id
    :param doctor_id:
    :return doctor:
    """
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        return doctor
    else:
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
        db.session.delete(doctor)
        db.session.commit()
    else:
        raise RuntimeError(f"Doctor with id: {doctor_id} was not found")
