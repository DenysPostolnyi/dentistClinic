import unittest
import requests


class PatientApiTestCase(unittest.TestCase):
    def test_get_all(self):
        response = requests.get("http://127.0.0.1:5000/patient-api")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_get_one(self):
        response_all = requests.get("http://127.0.0.1:5000/patient-api")
        id = response_all.json()[len(response_all.json()) - 1].get("patient_id")
        response_one = requests.get(f"http://127.0.0.1:5000/patient-api/{id}")
        self.assertEqual(response_one.status_code, 200)
        self.assertEqual(response_one.json(), response_all.json()[len(response_all.json()) - 1])

    def test_create(self):
        amount_before = len(requests.get("http://127.0.0.1:5000/patient-api").json())
        var = amount_before + 1
        patient_attrs = {
            "full_name": f"Test Patient{var}",
            "year_of_birth": 2000,
            "kind_of_ache": "MILD",
            "phone_number": f"09377817{var}",
            "email": f"testemail{var}@gmail.com"
        }
        response = requests.post("http://127.0.0.1:5000/patient-api", json=patient_attrs)
        amount_after = len(requests.get("http://127.0.0.1:5000/patient-api").json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(amount_before + 1, amount_after)

        response_take_all = requests.get("http://127.0.0.1:5000/patient-api")
        new_in_db = response_take_all.json()[len(response_take_all.json()) - 1]
        self.assertEqual(new_in_db['email'], patient_attrs['email'])

    def test_update(self):
        take_all = requests.get("http://127.0.0.1:5000/patient-api")
        var = len(take_all.json())
        patient_attrs = {
            "full_name": f"Test Patient{var}",
            "year_of_birth": 2004,
            "kind_of_ache": "MILD",
            "phone_number": f"06377817{var}",
            "email": f"testemail{var}@gmail.com"
        }
        patient_id = take_all.json()[len(take_all.json()) - 1].get('patient_id')
        response = requests.put(f"http://127.0.0.1:5000/patient-api/{patient_id}", json=patient_attrs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(patient_attrs['phone_number'], response.json()['phone_number'])
        self.assertEqual(patient_attrs['year_of_birth'], response.json()['year_of_birth'])

    def test_delete(self):
        take_all = requests.get("http://127.0.0.1:5000/patient-api")
        patient_id = take_all.json()[len(take_all.json()) - 1].get('patient_id')
        response = requests.delete(f"http://127.0.0.1:5000/patient-api/{patient_id}")
        self.assertEqual(response.status_code, 200)
