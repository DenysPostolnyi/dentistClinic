"""
Module for doctor's tests
"""
import json
import unittest
import requests

from tests.utils.for_api import delete_patient, delete_doctor, create_doctor, create_patient
from tests.utils import for_services
from src import app, Doctor
from src.service import doctor_service, patient_service


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
            "phone_number": f"09817{var}",
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
                "phone_number": f"0917{var}",
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


class DoctorServicesTestCase(unittest.TestCase):
    """
    Doctor Service test case
    """

    def test_get_all(self):
        """
        Test for service which get all doctors
        :return:
        """
        with app.app_context():
            doctors_list = doctor_service.get_all()
            self.assertIsNotNone(doctors_list)
            self.assertIs(list, type(doctors_list))

    def test_get_one_by_id(self):
        """
        Test for service which get doctor by id
        :return:
        """
        with app.app_context():
            doctors = doctor_service.get_all()
            if doctors is not None:
                doctor_id = doctors[0].doctor_id
                doctor = doctor_service.get_one_by_id(doctor_id)
                self.assertIsNotNone(doctor)
                self.assertEqual(doctors[0], doctor)

    def test_add(self):
        """
        Test for service which add new doctor
        :return:
        """
        with app.app_context():
            doctor_list = doctor_service.get_all()
            if len(doctor_list) > 0:
                val = doctor_list[len(doctor_list) - 1].doctor_id
            else:
                val = 0
            doctor_to_add = Doctor(
                full_name=f"Test Doctor{val}",
                seniority=3,
                specialty="ORTHOPEDIST",
                phone_number=f"0917{val}",
                email=f"testemail{val}@gmail.com"
            )
            new_doctor = doctor_service.add_doctors(doctor_to_add)
            self.assertEqual(doctor_to_add.full_name, new_doctor.full_name)
            doctor_service.delete(new_doctor.doctor_id)

    def test_count(self):
        """
        Test for service which count amount of doctors
        :return:
        """
        with app.app_context():
            doctors_list = doctor_service.get_all()
            doctor_amount = doctor_service.count_all()

            self.assertEqual(len(doctors_list), doctor_amount)

    def test_update(self):
        """
        Test for service which update doctor
        :return:
        """
        with app.app_context():
            doctor_list = doctor_service.get_all()
            if  len(doctor_list) > 0:
                val = doctor_list[len(doctor_list) - 1].doctor_id
            else:
                val = 0
            doctor_for_update = Doctor(
                full_name=f"Test Doctor{val}",
                seniority=3,
                specialty="ORTHOPEDIST",
                phone_number=f"0937{val}",
                email=f"testemail{val}@gmail.com"
            )
            doctor_for_update = doctor_service.add_doctors(doctor_for_update)
            doctor_for_update.email = "teste_update@gmail.com"
            doctor_service.update(doctor_for_update.doctor_id, doctor_for_update)
            self.assertEqual(doctor_for_update, doctor_service.get_one_by_id(doctor_for_update.doctor_id))
            doctor_service.delete(doctor_for_update.doctor_id)

    def test_delete(self):
        """
        Test for service which delete doctor
        :return:
        """
        with app.app_context():
            doctor_list = doctor_service.get_all()
            if  len(doctor_list) > 0:
                val = doctor_list[len(doctor_list) - 1].doctor_id
            else:
                val = 0
            doctor_for_delete = Doctor(
                full_name=f"Test Doctor{val}",
                seniority=3,
                specialty="ORTHOPEDIST",
                phone_number=f"0937{val}",
                email=f"testemail{val}@gmail.com"
            )
            doctor_for_delete = doctor_service.add_doctors(doctor_for_delete)
            doctor_service.delete(doctor_for_delete.doctor_id)
            self.assertNotIn(doctor_for_delete, doctor_service.get_all())

    def test_get_list_of_patients(self):
        """
        Test for service which get list of appointed patients to the doctor
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
            patient.date_of_appointment = "2023-02-02"
            self.assertEqual(patient.patient_id, doctor_service.get_list_of_patients(doctor.doctor_id)[0].patient_id)

            patient_service.delete(patient.patient_id)
            doctor_service.delete(doctor.doctor_id)

    def test_get_filtered_list_of_patients(self):
        """
        Test for service which get filtered list of appointed patients to the doctor by date
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

            date_for_search = {
                "date_from": "2023-01-02",
                "date_to": "2023-03-02",
            }

            self.assertEqual(patient.patient_id,
                             doctor_service.get_filtered_list_of_patients(doctor.doctor_id, date_for_search)[
                                 0].patient_id)

            date_for_search['date_to'] = "2023-02-01"

            self.assertEqual([], doctor_service.get_filtered_list_of_patients(doctor.doctor_id, date_for_search))

            patient_service.delete(patient.patient_id)
            doctor_service.delete(doctor.doctor_id)


class DoctorRoutesTestCase(unittest.TestCase):
    """
    Doctor Routes test case
    """
    def test_index(self):
        """
        Test for rout which return index page
        :return:
        """
        with app.test_client() as c:
            response = c.get('/doctors')
            self.assertEqual(200, response.status_code)

    def test_delete(self):
        """
        Test for rout which return index page
        :return:
        """
        doctor = for_services.create_doctor()
        with app.test_client() as c:
            response = c.get(f"/doctors/delete/{doctor.doctor_id}")
            self.assertEqual(302, response.status_code)

    def test_info(self):
        """
        Test for rout which return index page
        :return:
        """
        doctor = for_services.create_doctor()
        with app.test_client() as c:
            response = c.get(f"/doctors/{doctor.doctor_id}")
            self.assertEqual(200, response.status_code)
            c.get(f"/doctors/delete/{doctor.doctor_id}")

    def test_filter(self):
        """
        Test for rout for page with info about doctor where list appointed patients filtered by date of appointment
        :return:
        """
        doctor = for_services.create_doctor()
        with app.test_client() as c:
            response = c.post(f"/doctors/{doctor.doctor_id}", data={
                "date_from": "2023-02-03",
                "date_to": "2023-02-15"
            })
            self.assertEqual(200, response.status_code)

            c.get(f"/doctors/delete/{doctor.doctor_id}")

    def test_add(self):
        """
        Test for rout for page for adding new doctor
        :return:
        """
        with app.test_client() as c:
            # Test get
            response = c.get("/doctors/add")
            self.assertEqual(200, response.status_code)

            # Test post
            response_all = requests.get("http://127.0.0.1:5000/doctor-api",
                                        timeout=1000)
            if isinstance(response_all.json(), dict) and "message" in response_all.json().keys():
                self.assertEqual("Doctor list is empty", response_all.json().get("message"))
                amount_before = 0
            else:
                amount_before = len(response_all.json())

            var = amount_before + 1

            response = c.post("/doctors/add", data={
                "full_name": f"Test Doctor{var}",
                "seniority": 3,
                "specialty": "ORTHOPEDIST",
                "phone_number": f"09817{var}",
                "email": f"testemail{var}@gmail.com"
            })
            self.assertEqual(302, response.status_code)

    def test_edit(self):
        """
        Test for rout for page for editing info about doctor
        :return:
        """
        response_all = requests.get("http://127.0.0.1:5000/doctor-api",
                                    timeout=1000)
        if isinstance(response_all.json(), dict) and "message" in response_all.json().keys():
            amount_before = 0
        else:
            amount_before = len(response_all.json())

        var = amount_before + 1

        created_doctor = requests.post("http://127.0.0.1:5000/doctor-api", json={
            "full_name": f"Test Doctor{var}",
            "seniority": 3,
            "specialty": "ORTHOPEDIST",
            "phone_number": f"09817{var}",
            "email": f"testemail{var}@gmail.com"
        }, timeout=1000).json()['doctor']
        with app.test_client() as c:
            # Test get
            response = c.get(f"/doctors-edit/{created_doctor['doctor_id']}")
            self.assertEqual(200, response.status_code)

            # Test post
            response = c.post(f"/doctors-edit/{created_doctor['doctor_id']}", data={
                "full_name": f"Test Doctor{var}",
                "seniority": 3,
                "specialty": "ORTHOPEDIST",
                "phone_number": f"09817{var}",
                "email": f"updated-email{var}@gmail.com"
            })
            self.assertEqual(302, response.status_code)

            requests.delete(f"http://127.0.0.1:5000/doctor-api/{created_doctor['doctor_id']}",
                            timeout=1000)
