from src import app, Doctor, Patient
from src.service import doctor_service, patient_service


def create_doctor():
    with app.app_context():
        doctor_list = doctor_service.get_all()
        if doctor_list is not None:
            val = doctor_list[len(doctor_list) - 1].doctor_id
        else:
            val = 0
        doctor = Doctor(
            full_name=f"Test Doctor{val}",
            seniority=3,
            specialty="ORTHOPEDIST",
            phone_number=f"0937{val}",
            email=f"testemail{val}@gmail.com"
        )
        return doctor_service.add_doctors(doctor)


def create_patient():
    with app.app_context():
        patients_list = patient_service.get_all()
        if patients_list is not None:
            patient_val = patients_list[len(patients_list) - 1].patient_id
        else:
            patient_val = 0

        patient = Patient(
            full_name=f"Test Patient{patient_val}",
            year_of_birth=2000,
            kind_of_ache="MILD",
            phone_number=f"09817{patient_val}",
            email=f"testemail{patient_val}@gmail.com"
        )

        return patient_service.add_patient(patient)
