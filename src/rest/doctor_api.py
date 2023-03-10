"""
Doctor API
"""
import json
import logging

from flask import abort, Flask, Blueprint, request
from flask_restful import Resource, Api
from src.service import doctor_service
from src.util import doctor_mapper

app = Flask(__name__)
api_doctor = Blueprint('doctor_api', __name__)
api = Api(api_doctor)


class DoctorAPIGetPost(Resource):
    """
    Class for receiving GET and POST methods without params
    """

    def get(self):
        """
        Get method for getting all doctors from DB
        :return JSON list of Doctor objects:
        """
        doctors = doctor_service.get_all()
        if doctors:
            logging.debug("All doctors was gotten: %s", doctors)
            return [json.loads(obj.to_json()) for obj in doctors]
        logging.debug("Tried get all doctors but doctors list is empty")
        return {"message": "Doctor list is empty"}

    def post(self):
        """
        Get method for adding new doctor to DB
        :return JSON message of success
        """
        new_doctor = request.get_json(force=True)
        doctor = doctor_mapper.json_to_doctor(new_doctor)
        answer = doctor_service.add_doctors(doctor)
        logging.debug("New doctor was added to DB: %s", doctor)

        return {"message": "Doctor was added successfully", "doctor": json.loads(answer.to_json())}


class DoctorAPICount(Resource):
    """
    Class for GET method that returns amount of doctors
    """
    def get(self):
        """
        Method call service that counts amount of doctors
        :return:
        """
        doctors = doctor_service.get_all()
        if doctors:
            return {
                "amount": doctor_service.count_all()
            }
        return {"message": "Doctor list is empty"}


class DoctorAPIGetUpdateDelete(Resource):
    """
    Class for receiving GET and PUT DELETE methods with parameter id
    """

    def get(self, doctor_id):
        """
         Get method for getting doctor from DB by id
        :param doctor_id:
        :return JSON Doctor object:
        :except Doctor was not found:
        """
        try:
            doctor = doctor_service.get_one_by_id(doctor_id)
            logging.debug("Doctor by id - %s was gotten, doctor: %s", doctor_id, doctor)
            return json.loads(doctor.to_json())
        except RuntimeError as error:
            logging.debug("Doctor by id - %s was not found", doctor_id)
            abort(404, str(error))

    def put(self, doctor_id):
        """
        Put method for editing doctor in DB by id
        :param doctor_id:
        :return JSON Doctor object:
        :except Doctor was not found:
        """
        new_doctor = request.get_json(force=True)
        doctor = doctor_mapper.json_to_doctor(new_doctor)
        try:
            doctor_service.update(doctor_id, doctor)
            doctor.doctor_id = doctor_id
            logging.debug("Doctor by id - %s was updated, new doctor: %s", doctor_id, doctor)
            return json.loads(doctor.to_json())
        except RuntimeError as error:
            logging.debug("Doctor for update by id - %s was not found", doctor_id)
            abort(404, str(error))

    def delete(self, doctor_id):
        """
        Put method for editing doctor in DB by id
        :param doctor_id:
        :return JSON Doctor object:
        :except Doctor was not found:
        """
        try:
            doctor_service.delete(doctor_id)
            logging.debug("Doctor by id - %s was deleted", doctor_id)
            return {"message": "Doctor was successfully deleted"}
        except RuntimeError as error:
            logging.debug("Doctor for delete by id - %s was not found", doctor_id)
            abort(404, str(error))


class DoctorAPIClients(Resource):
    """
    Class for getting info about appointed patients
    """
    def get(self, doctor_id):
        """
        Method for getting all appointed patients to the doctor
        :param doctor_id:
        :return: list of appointed patients
        """
        try:
            ls = [json.loads(obj.to_json()) for obj in doctor_service.get_list_of_patients(doctor_id)]
            logging.debug("List of appointed patients to doctor with id: %s was gotten", doctor_id)
            return ls
        except RuntimeError as error:
            logging.debug("Doctor by id - %s was not found", doctor_id)
            abort(404, str(error))

    def post(self, doctor_id):
        """
        Method for getting all appointed patients to the doctor from one time to another
        :param doctor_id:
        :return: list of appointed patients searched by time
        """
        try:
            date = request.get_json(force=True)
            ls = [json.loads(obj.to_json()) for obj in doctor_service.get_filtered_list_of_patients(doctor_id, date)]
            logging.debug("List of appointed patients from date %s, to %s to doctor with id: %s was gotten",
                          date["date_from"], date["date_to"], doctor_id)
            return ls
        except RuntimeError as error:
            logging.debug("Doctor by id - %s was not found", doctor_id)
            abort(404, str(error))


api.add_resource(DoctorAPIGetPost, '/doctor-api')
api.add_resource(DoctorAPICount, '/doctor-api/count')
api.add_resource(DoctorAPIGetUpdateDelete, '/doctor-api/<doctor_id>')
api.add_resource(DoctorAPIClients, '/doctor-api/clients/<doctor_id>')
