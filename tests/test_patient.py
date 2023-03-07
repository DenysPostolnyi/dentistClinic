"""
Module for patient's tests
"""
import unittest
import requests

from src import app, Patient
from src.service import patient_service, doctor_service
from tests.test_doctor import create_patient, delete_patient, delete_doctor, create_doctor
from tests.test_doctor import for_services


class PatientApiTestCase(unittest.TestCase):
    """
    Patient API test case
    """

    def test_get_all(self):
        """
        Test getting all patients
        :return:
        """
        response = requests.get("http://127.0.0.1:5000/patient-api", timeout=1000)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_get_one(self):
        """
        Test getting one patient
        :return:
        """
        response_all = requests.get("http://127.0.0.1:5000/patient-api", timeout=1000)
        if isinstance(response_all.json(), dict) and "message" in response_all.json().keys():
            self.assertEqual(response_all.json().get("message"), "Patient list is empty")
        else:
            patient_id = response_all.json()[len(response_all.json()) - 1].get("patient_id")
            response_one = requests.get(f"http://127.0.0.1:5000/patient-api/{patient_id}", timeout=1000)
            self.assertEqual(response_one.status_code, 200)
            self.assertEqual(response_one.json(), response_all.json()[len(response_all.json()) - 1])

    def test_create(self):
        """
        Test creating patient
        :return:
        """
        response_all = requests.get("http://127.0.0.1:5000/patient-api", timeout=1000)
        if isinstance(response_all.json(), dict) and "message" in response_all.json().keys():
            self.assertEqual(response_all.json().get("message"), "Patient list is empty")
            amount_before = 0
        else:
            amount_before = len(response_all.json())

        var = amount_before + 1
        patient_attrs = {
            "full_name": f"Test Patient{var}",
            "year_of_birth": 2000,
            "kind_of_ache": "MILD",
            "phone_number": f"09377817{var}",
            "email": f"testemail{var}@gmail.com"
        }
        response = requests.post("http://127.0.0.1:5000/patient-api", json=patient_attrs, timeout=1000)
        amount_after = len(requests.get("http://127.0.0.1:5000/patient-api", timeout=1000).json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(amount_before + 1, amount_after)

        response_take_all = requests.get("http://127.0.0.1:5000/patient-api", timeout=1000)
        new_in_db = response_take_all.json()[len(response_take_all.json()) - 1]
        self.assertEqual(new_in_db['email'], patient_attrs['email'])

    def test_update(self):
        """
        Test update patient
        :return:
        """
        take_all = requests.get("http://127.0.0.1:5000/patient-api", timeout=1000)
        if isinstance(take_all.json(), dict) and "message" in take_all.json().keys():
            self.assertEqual(take_all.json().get("message"), "Patient list is empty")
        else:
            var = len(take_all.json())
            patient_attrs = {
                "full_name": f"Test Patient{var}",
                "year_of_birth": 2004,
                "kind_of_ache": "MILD",
                "phone_number": f"06377817{var}",
                "email": f"testemail{var}@gmail.com"
            }
            patient_id = take_all.json()[len(take_all.json()) - 1].get('patient_id')
            response = requests.put(f"http://127.0.0.1:5000/patient-api/{patient_id}", json=patient_attrs, timeout=1000)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(patient_attrs['phone_number'], response.json()['phone_number'])
            self.assertEqual(patient_attrs['year_of_birth'], response.json()['year_of_birth'])

    def test_delete(self):
        """
        Test delete patient
        :return:
        """
        take_all = requests.get("http://127.0.0.1:5000/patient-api", timeout=1000)
        if isinstance(take_all.json(), dict) and "message" in take_all.json().keys():
            self.assertEqual(take_all.json().get("message"), "Patient list is empty")
        else:
            patient_id = take_all.json()[len(take_all.json()) - 1].get('patient_id')
            response = requests.delete(f"http://127.0.0.1:5000/patient-api/{patient_id}", timeout=1000)
            self.assertEqual(response.status_code, 200)

    def test_make_appoint(self):
        """
        Test appoint person
        :return:
        """
        # creating doctor
        response_create_doctor = create_doctor()

        # creating patient
        response_create_patient = create_patient()

        # appoint patient
        data = {
            'doctor_id': int(response_create_doctor.json()['doctor']['doctor_id']),
            'date_of_appointment': "2023-02-02"
        }
        requests.post(
            f"http://127.0.0.1:5000/patient-api/appoint/{response_create_patient.json()['patient']['patient_id']}",
            json=data,
            timeout=1000)

        # taking appointed patient
        appointed_patient = requests.get(
            f"http://127.0.0.1:5000/patient-api/{int(response_create_patient.json()['patient']['patient_id'])}",
            timeout=1000)

        if appointed_patient.status_code == 200:
            self.assertEqual(response_create_patient.json()['patient']['email'], appointed_patient.json()['email'])
            self.assertIsNotNone(appointed_patient.json()['doctor_id'])
            self.assertEqual(response_create_doctor.json()['doctor']['doctor_id'],
                             appointed_patient.json()['doctor_id'])

        # delete all
        delete_patient(response_create_patient.json()['patient']['patient_id'])
        delete_doctor(response_create_doctor.json()['doctor']['doctor_id'])

    def test_cancel_appoint(self):
        """
        Test appoint person
        :return:
        """
        # creating doctor
        response_create_doctor = create_doctor()

        # creating patient
        response_create_patient = create_patient()

        # appoint patient
        data = {
            'doctor_id': int(response_create_doctor.json()['doctor']['doctor_id']),
            'date_of_appointment': "2023-02-02"
        }
        requests.post(
            f"http://127.0.0.1:5000/patient-api/appoint/{response_create_patient.json()['patient']['patient_id']}",
            json=data,
            timeout=1000)

        requests.delete(
            f"http://127.0.0.1:5000/patient-api/appoint/{response_create_patient.json()['patient']['patient_id']}",
            timeout=1000)

        # taking appointed patient
        appointed_patient = requests.get(
            f"http://127.0.0.1:5000/patient-api/{int(response_create_patient.json()['patient']['patient_id'])}",
            timeout=1000)

        if appointed_patient.status_code == 200:
            self.assertEqual(response_create_patient.json()['patient']['email'], appointed_patient.json()['email'])
            self.assertIsNone(appointed_patient.json()['doctor_id'])

        # delete all
        delete_patient(response_create_patient.json()['patient']['patient_id'])
        delete_doctor(response_create_doctor.json()['doctor']['doctor_id'])


class PatientServicesTestCase(unittest.TestCase):
    """
    Patient Service test case
    """
    def test_get_all(self):
        """
        Test for service which get all patients
        :return:
        """
        with app.app_context():
            patients_list = patient_service.get_all()
            self.assertIsNotNone(patients_list)
            self.assertIs(list, type(patients_list))

    def test_get_one_by_id(self):
        """
        Test for service which get patient by id
        :return:
        """
        with app.app_context():
            patients = patient_service.get_all()
            if patients is not None:
                patient_id = patients[0].patient_id
                patient = patient_service.get_one_by_id(patient_id)
                self.assertIsNotNone(patient)
                self.assertEqual(patients[0], patient)

    def test_add(self):
        """
        Test for service which add new patient
        :return:
        """
        with app.app_context():
            patients_list = patient_service.get_all()
            if patients_list is not None:
                val = patients_list[len(patients_list) - 1].patient_id
            else:
                val = 0
            patient_to_add = Patient(
                full_name=f"Test Patient{val}",
                year_of_birth=2002,
                kind_of_ache="MILD",
                phone_number=f"0917{val}",
                email=f"testemail{val}@gmail.com"
            )
            new_patient = patient_service.add_patient(patient_to_add)
            self.assertEqual(patient_to_add.full_name, new_patient.full_name)
            patient_service.delete(new_patient.patient_id)

    def test_update(self):
        """
        Test for service which update patient
        :return:
        """
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
            patient_for_update = patient_service.add_patient(patient)
            patient_for_update.email = "teste_update@gmail.com"
            patient_service.update(patient_for_update.patient_id, patient_for_update)
            self.assertEqual(patient_for_update, patient_service.get_one_by_id(patient_for_update.patient_id))
            patient_service.delete(patient_for_update.patient_id)

    def test_delete(self):
        """
        Test for service which delete patient
        :return:
        """
        with app.app_context():
            patient_for_delete = for_services.create_patient()
            patient_service.delete(patient_for_delete.patient_id)
            self.assertNotIn(patient_for_delete, patient_service.get_all())

    def test_make_appointment(self):
        """
        Test for service which makes appointment
        :return:
        """
        with app.app_context():
            doctor = for_services.create_doctor()
            patient = for_services.create_patient()

            # appoint patient
            data = {
                'doctor_id': int(doctor.doctor_id),
                'date_of_appointment': "2023-02-02"
            }

            patient_service.make_appointment(patient.patient_id, data)

            self.assertEqual("2023-02-02", str(patient_service.get_one_by_id(patient.patient_id).date_of_appointment))

            patient_service.delete(patient.patient_id)
            doctor_service.delete(doctor.doctor_id)

    def test_cancel_appointment(self):
        """
        Test for service which cancel appointment
        :return:
        """
        with app.app_context():
            doctor = for_services.create_doctor()
            patient = for_services.create_patient()

            # appoint patient
            data = {
                'doctor_id': int(doctor.doctor_id),
                'date_of_appointment': "2023-02-02"
            }

            patient_service.make_appointment(patient.patient_id, data)
            patient_service.cancel_appointment(patient.patient_id)

            self.assertEqual(None, patient_service.get_one_by_id(patient.patient_id).date_of_appointment)

            patient_service.delete(patient.patient_id)
            doctor_service.delete(doctor.doctor_id)
