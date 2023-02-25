import unittest

from src import create_app
from src.models.models import Doctor, Specialty
from src.service import doctor_service


class TestDB(unittest.TestCase):
    def test_get_doctor(self):
        with create_app().app_context():
            doctor = Doctor(full_name="Derek", seniority=4, specialty=Specialty.THERAPIST, phone_number="0636582647",
                            email="email2@gmail.com")
            # doctor_service.add_doctors(doctor)
            self.assertIsNotNone(doctor_service.get_all())
