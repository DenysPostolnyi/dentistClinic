"""
Module for doctor's tests
"""
import unittest
import requests


class DoctorApiTestCase(unittest.TestCase):
    """
    Doctor API test case
    """

    def test_get_all(self):
        """
        Test getting all doctors
        :return:
        """
        response = requests.get("http://127.0.0.1:5000/doctor-api")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_get_one(self):
        """
        Test getting one doctor
        :return:
        """
        response_all = requests.get("http://127.0.0.1:5000/doctor-api")
        if response_all.json()[0].get("doctor_id"):
            id = response_all.json()[len(response_all.json()) - 1].get("doctor_id")
            response_one = requests.get(f"http://127.0.0.1:5000/doctor-api/{id}")
            self.assertEqual(response_one.status_code, 200)
            self.assertEqual(response_one.json(), response_all.json()[len(response_all.json()) - 1])
        else:
            self.assertEqual(response_all.json().get("message"), "Doctor list is empty")

    def test_create(self):
        """
        Test creating doctor
        :return:
        """
        amount_before = len(requests.get("http://127.0.0.1:5000/doctor-api").json())
        var = amount_before + 1
        doctor_attrs = {
            "full_name": f"Test Doctor{var}",
            "seniority": 3,
            "specialty": "ORTHOPEDIST",
            "phone_number": f"09377817{var}",
            "email": f"testemail{var}@gmail.com"
        }
        response = requests.post("http://127.0.0.1:5000/doctor-api", json=doctor_attrs)
        amount_after = len(requests.get("http://127.0.0.1:5000/doctor-api").json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(amount_before + 1, amount_after)

        response_take_all = requests.get("http://127.0.0.1:5000/doctor-api")
        new_in_db = response_take_all.json()[len(response_take_all.json()) - 1]
        self.assertEqual(new_in_db['email'], doctor_attrs['email'])

    def test_update(self):
        """
        Test update doctor
        :return:
        """
        take_all = requests.get("http://127.0.0.1:5000/doctor-api")
        var = len(take_all.json())
        doctor_attrs = {
            "full_name": f"Test Doctor{var}",
            "seniority": 4,
            "specialty": "ORTHOPEDIST",
            "phone_number": f"09472817{var}",
            "email": f"my_testemail{var}@gmail.com"
        }
        doctor_id = take_all.json()[len(take_all.json()) - 1].get('doctor_id')
        response = requests.put(f"http://127.0.0.1:5000/doctor-api/{doctor_id}", json=doctor_attrs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(doctor_attrs['phone_number'], response.json()['phone_number'])
        self.assertEqual(doctor_attrs['seniority'], response.json()['seniority'])

    def test_delete(self):
        """
        Test delete doctor
        :return:
        """
        take_all = requests.get("http://127.0.0.1:5000/doctor-api")
        doctor_id = take_all.json()[len(take_all.json()) - 1].get('doctor_id')
        response = requests.delete(f"http://127.0.0.1:5000/doctor-api/{doctor_id}")
        self.assertEqual(response.status_code, 200)
