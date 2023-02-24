import unittest

from src.service import doctor_service
from src import create_app, DBSettings


class TestDB(unittest.TestCase):
    def test_get_doctor(self):
        print(DBSettings.SQLALCHEMY_DATABASE_URL)
        with create_app().app_context():
            self.assertIsNotNone(doctor_service.get_one_by_id(2))
