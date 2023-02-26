from src.models.models import Patient, KindOfAche


def json_to_patient(response):
    patient = Patient(full_name=response.get("full_name"), year_of_birth=response.get("year_of_birth"),
                    kind_of_ache=KindOfAche[response.get("kind_of_ache")], phone_number=response.get("phone_number"),
                    email=response.get("email"))

    return patient
