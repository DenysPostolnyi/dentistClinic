"""
Models for entities
"""
import enum
import json

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


class Specialty(enum.Enum):
    """
    Enum with kinds of specialty
    """
    THERAPIST = 'therapist'
    ORTHOPEDIST = 'orthopedist'
    SURGEON = 'surgeon'
    RADIOLOGIST = 'radiologist'


class Doctor(db.Model):
    """
    Class for doctor entity
    """
    __tablename__ = "Doctors"
    doctor_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=True)
    seniority = db.Column(db.Integer)
    specialty = db.Column(db.Enum(Specialty))
    phone_number = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f"({self.full_name}, {self.seniority}, {self.specialty}, " \
               f"{self.phone_number}, {self.email})"

    def to_json(self):
        return json.dumps({
            "doctor_id": self.doctor_id,
            "full_name": self.full_name,
            "seniority": self.seniority,
            "specialty": self.specialty.__str__(),
            "phone_number": self.phone_number,
            "email": self.email,
        })


class KindOfAche(enum.Enum):
    """
    Enum for kinds of ache
    """
    NONE = 'none'
    MILD = 'mild'
    MIDDLE = 'middle'
    STRONG = 'strong'


class Patient(db.Model):
    """
    Class for patient entity
    """
    __tablename__ = "Patients"
    patient_id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.ForeignKey("Doctors.doctor_id"))
    full_name = db.Column(db.String(100), unique=True)
    year_of_birth = db.Column(db.Integer)
    kind_of_ache = db.Column(db.Enum(KindOfAche))
    phone_number = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f"({self.full_name}, {self.year_of_birth}, {self.kind_of_ache}, " \
               f"{self.phone_number}, {self.email})"

    def to_json(self):
        return json.dumps({
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "full_name": self.full_name,
            "year_of_birth": self.year_of_birth,
            "kind_of_ache": self.kind_of_ache.__str__(),
            "phone_number": self.phone_number,
            "email": self.email,
        })