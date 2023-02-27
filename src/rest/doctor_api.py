import json

from flask import abort, Flask, Blueprint, request
from flask_restful import Resource, Api
from src.service import doctor_service
from src.util import doctor_mapper
import logging

app = Flask(__name__)
api_doctor = Blueprint('doctor_api', __name__)
api = Api(api_doctor)


class DoctorAPIGetPost(Resource):
    def get(self):
        doctors = doctor_service.get_all()
        if doctors:
            logging.debug("All doctors was gotten: %s", doctors)
            return [json.loads(obj.to_json()) for obj in doctors]
        else:
            logging.debug("Tried get all doctors but doctors list is empty")
            abort(404, "Doctors were not found")

    def post(self):
        new_doctor = request.get_json(force=True)
        doctor = doctor_mapper.json_to_doctor(new_doctor)
        doctor_service.add_doctors(doctor)
        logging.debug("New doctor was added to DB: %s", doctor)
        return {"message": "Doctor was added successfully"}


class DoctorAPIGetUpdateDelete(Resource):
    def get(self, id):
        try:
            doctor = doctor_service.get_one_by_id(id)
            logging.debug("Doctor by id - %s was gotten, doctor: %s", id, doctor)
            return json.loads(doctor.to_json())
        except RuntimeError as error:
            logging.debug("Doctor by id - %s was not found", id)
            abort(404, str(error))

    def put(self, id):
        new_doctor = request.get_json(force=True)
        doctor = doctor_mapper.json_to_doctor(new_doctor)
        try:
            doctor_service.update(id, doctor)
            doctor.doctor_id = id
            logging.debug("Doctor by id - %s was updated, new doctor: %s", id, doctor)
            return json.loads(doctor.to_json())
        except RuntimeError as error:
            logging.debug("Doctor for update by id - %s was not found", id)
            abort(404, str(error))

    def delete(self, id):
        try:
            doctor_service.delete(id)
            logging.debug("Doctor by id - %s was deleted", id)
            return {"message": "Doctor was successfully deleted"}
        except RuntimeError as error:
            logging.debug("Doctor for delete by id - %s was not found", id)
            abort(404, str(error))


api.add_resource(DoctorAPIGetPost, '/doctor-api')
api.add_resource(DoctorAPIGetUpdateDelete, '/doctor-api/<id>')
