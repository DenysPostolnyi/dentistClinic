"""
Helping module for doctor
"""
from src.models.models import Doctor, Specialty


def json_to_doctor(response):
    """
    Function for parsing JSON and make Doctor object
    :param response:
    :return Doctor:
    """
    doctor = Doctor(full_name=response.get("full_name"), seniority=response.get("seniority"),
                    specialty=Specialty[response.get("specialty")], phone_number=response.get("phone_number"),
                    email=response.get("email"))

    return doctor
