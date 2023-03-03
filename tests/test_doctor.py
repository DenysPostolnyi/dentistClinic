"""
Module for doctor's tests
"""
import unittest
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
    response_delete_doctor = requests.delete(
        f"http://127.0.0.1:5000/doctor-api/{doctor_id}",
        timeout=1000)


def delete_patient(patient_id):
    response_delete_patient = requests.delete(
        f"http://127.0.0.1:5000/patient-api/{patient_id}",
        timeout=1000)


class DoctorApiTestCase(unittest.TestCase):
    """
    Doctor API test case
    """

    def test_get_all(self):
        """
        Test getting all doctors
        :return:
        """
        response = requests.get("http://127.0.0.1:5000/doctor-api",
                                timeout=1000)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json())

    def test_get_one(self):
        """
        Test getting one doctor
        :return:
        """
        response_all = requests.get("http://127.0.0.1:5000/doctor-api",
                                    timeout=1000)
        if isinstance(response_all.json(), dict) and "message" in response_all.json().keys():
            self.assertEqual("Doctor list is empty", response_all.json().get("message"))
        else:
            id = response_all.json()[len(response_all.json()) - 1].get("doctor_id")
            response_one = requests.get(f"http://127.0.0.1:5000/doctor-api/{id}",
                                        timeout=1000)
            self.assertEqual(200, response_one.status_code)
            self.assertEqual(response_all.json()[len(response_all.json()) - 1], response_one.json())

    def test_create(self):
        """
        Test creating doctor
        :return:
        """
        response_all = requests.get("http://127.0.0.1:5000/doctor-api",
                                    timeout=1000)
        if isinstance(response_all.json(), dict) and "message" in response_all.json().keys():
            self.assertEqual("Doctor list is empty", response_all.json().get("message"))
            amount_before = 0
        else:
            amount_before = len(response_all.json())

        var = amount_before + 1
        doctor_attrs = {
            "full_name": f"Test Doctor{var}",
            "seniority": 3,
            "specialty": "ORTHOPEDIST",
            "phone_number": f"09377817{var}",
            "email": f"testemail{var}@gmail.com"
        }
        response = requests.post("http://127.0.0.1:5000/doctor-api", json=doctor_attrs,
                                 timeout=1000)
        amount_after = len(requests.get("http://127.0.0.1:5000/doctor-api",
                                        timeout=1000).json())
        self.assertEqual(200, response.status_code)
        self.assertEqual(amount_before + 1, amount_after)

        response_take_all = requests.get("http://127.0.0.1:5000/doctor-api",
                                         timeout=1000)
        new_in_db = response_take_all.json()[len(response_take_all.json()) - 1]
        self.assertEqual(new_in_db['email'], doctor_attrs['email'])

    def test_update(self):
        """
        Test update doctor
        :return:
        """
        take_all = requests.get("http://127.0.0.1:5000/doctor-api",
                                timeout=1000)
        if isinstance(take_all.json(), dict) and "message" in take_all.json().keys():
            self.assertEqual("Doctor list is empty", take_all.json().get("message"))
        else:
            var = len(take_all.json())
            doctor_attrs = {
                "full_name": f"Test Doctor{var}",
                "seniority": 4,
                "specialty": "ORTHOPEDIST",
                "phone_number": f"09472817{var}",
                "email": f"my_testemail{var}@gmail.com"
            }
            doctor_id = take_all.json()[len(take_all.json()) - 1].get('doctor_id')
            response = requests.put(f"http://127.0.0.1:5000/doctor-api/{doctor_id}", json=doctor_attrs,
                                    timeout=1000)
            self.assertEqual(200, response.status_code)
            self.assertEqual(response.json()['phone_number'], doctor_attrs['phone_number'])
            self.assertEqual(response.json()['seniority'], doctor_attrs['seniority'])

    def test_delete(self):
        """
        Test delete doctor
        :return:
        """
        take_all = requests.get("http://127.0.0.1:5000/doctor-api",
                                timeout=1000)
        if isinstance(take_all.json(), dict) and "message" in take_all.json().keys():
            self.assertEqual("Doctor list is empty", take_all.json().get("message"))
        else:
            doctor_id = take_all.json()[len(take_all.json()) - 1].get('doctor_id')
            response = requests.delete(f"http://127.0.0.1:5000/doctor-api/{doctor_id}",
                                       timeout=1000)
            self.assertEqual(200, response.status_code)

    def test_count(self):
        """
        Test counting all doctors
        :return:
        """
        take_all = requests.get("http://127.0.0.1:5000/doctor-api",
                                timeout=1000)
        if isinstance(take_all.json(), dict) and "message" in take_all.json().keys():
            self.assertEqual("Doctor list is empty", take_all.json().get("message"))
        elif take_all.status_code == 200:
            count = requests.get("http://127.0.0.1:5000/doctor-api/count",
                                 timeout=1000)
            if count.status_code == 200:
                self.assertEqual(len(take_all.json()), count.json()['amount'])
            else:
                self.assertEqual("Doctor list is empty", count.json()['amount'])

    def test_take_patients(self):
        """
        Test getting all appointed patients
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

        # taking appointed patients
        appointed_patients = requests.get(
            f"http://127.0.0.1:5000/doctor-api/clients/{int(response_create_doctor.json()['doctor']['doctor_id'])}",
            timeout=1000)

        if appointed_patients.status_code == 200:
            self.assertIsNotNone(appointed_patients.json())
            self.assertEqual(response_create_patient.json()['patient']['email'], appointed_patients.json()[0]['email'])

        # delete all
        delete_patient(response_create_patient.json()['patient']['patient_id'])
        delete_doctor(response_create_doctor.json()['doctor']['doctor_id'])

    def test_take_filtered_patients(self):
        """
        Test getting appointed patients filtered by date of appoint
        :return:
        """
        created_patient = create_patient()
        created_doctor = create_doctor()

        # appoint patient
        data = {
            'doctor_id': int(created_doctor.json()['doctor']['doctor_id']),
            'date_of_appointment': "2023-02-02"
        }
        requests.post(
            f"http://127.0.0.1:5000/patient-api/appoint/{created_patient.json()['patient']['patient_id']}",
            json=data,
            timeout=1000)

        # taking appointed patients(show)
        data = {
            "time_before": "2023-02-01",
            "time_after": "2023-02-03"
        }
        appointed_patients = requests.post(
            f"http://127.0.0.1:5000/doctor-api/clients/{int(created_doctor.json()['doctor']['doctor_id'])}",
            json=data,
            timeout=1000)

        if appointed_patients.status_code == 200:
            self.assertIsNotNone(appointed_patients.json())
            self.assertEqual(created_patient.json()['patient']['email'], appointed_patients.json()[0]['email'])

        data = {
            "time_before": "2023-01-01",
            "time_after": "2023-02-01"
        }
        appointed_patients = requests.post(
            f"http://127.0.0.1:5000/doctor-api/clients/{int(created_doctor.json()['doctor']['doctor_id'])}",
            json=data,
            timeout=1000)

        if appointed_patients.status_code == 200:
            self.assertIsNotNone(appointed_patients.json())

        delete_patient(created_patient.json()['patient']['patient_id'])
        delete_doctor(created_doctor.json()['doctor']['doctor_id'])
