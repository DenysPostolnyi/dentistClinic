from src.models.models import Doctor, Specialty


def json_to_doctor(response):
    doctor = Doctor(full_name=response.get("full_name"), seniority=response.get("seniority"),
                    specialty=Specialty[response.get("specialty")], phone_number=response.get("phone_number"),
                    email=response.get("email"))

    return doctor
