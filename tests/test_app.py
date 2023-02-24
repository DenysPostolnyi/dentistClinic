import unittest

from src.models.models import Doctor
from src.service import doctor_service
from src import create_app


class TestDB(unittest.TestCase):
    def test_get_doctor(self):
        with create_app().app_context():
            self.assertIsNotNone(Doctor.query.get_or_404(2))
