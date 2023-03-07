"""
Helping module for patient
"""
from src.models.models import Patient, KindOfAche


def json_to_patient(response):
    """
    Function for parsing JSON and make Patient object
    :param response:
    :return Patient:
    """
    patient = Patient(full_name=response.get("full_name"),
                      year_of_birth=response.get("year_of_birth"),
                      kind_of_ache=KindOfAche[response.get("kind_of_ache")],
                      phone_number=response.get("phone_number"), email=response.get("email"),
                      date_of_appointment=response.get("date_of_appointment"))

    return patient
