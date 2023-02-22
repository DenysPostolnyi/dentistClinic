from src.models.models import db, Doctor


def add_doctors(doctor):
    db.session.add(doctor)
    db.session.commit()


def get_all():
    return Doctor.query.all()


def get_one_by_id(doctor_id):
    return Doctor.query.get_or_404(doctor_id)


def update(doctor_id, doctor):
    doctor_for_edit = Doctor.query.get_or_404(doctor_id)

    doctor_for_edit.full_name = doctor.full_name
    doctor_for_edit.seniority = doctor.seniority
    doctor_for_edit.specialty = doctor.specialty
    doctor_for_edit.phone_number = doctor.phone_number
    doctor_for_edit.email = doctor.email

    db.session.add(doctor_for_edit)
    db.session.commit()


def delete(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
