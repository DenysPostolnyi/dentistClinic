"""
Module for patient's tests
"""
import unittest
import requests

from tests.test_doctor import create_patient, delete_patient, delete_doctor, create_doctor


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
