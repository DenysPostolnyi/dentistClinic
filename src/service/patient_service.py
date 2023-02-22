from src.models.models import db, Patient


def add_patient(patient):
    db.session.add(patient)
    db.session.commit()


def get_all():
    return Patient.query.all()


def get_one_by_id(patient_id):
    return Patient.query.get_or_404(patient_id)


def update(patient_id, patient):
    patient_for_edit = Patient.query.get_or_404(patient_id)
    patient_for_edit.full_name = patient.full_name
    patient_for_edit.year_of_birth = patient.year_of_birth
    patient_for_edit.kind_of_ache = patient.kind_of_ache
    patient_for_edit.phone_number = patient.phone_number
    patient_for_edit.email = patient.email

    db.session.add(patient_for_edit)
    db.session.commit()


def delete(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
