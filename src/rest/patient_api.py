"""
Patient API
"""
import json
import logging

from flask import abort, Flask, Blueprint, request
from flask_restful import Resource, Api
from src.service import patient_service
from src.util import patient_mapper

app = Flask(__name__)
api_patient = Blueprint('patient_api', __name__)
api = Api(api_patient)


class PatientAPIGetPost(Resource):
    """
    Class for receiving GET and POST methods without params
    """

    def get(self):
        """
        Get method for getting all patients from DB
        :return JSON list of Patient objects:
        """
        patients = patient_service.get_all()
        if patients:
            logging.debug("All patients was gotten: %s", patients)
            return [json.loads(obj.to_json()) for obj in patients]
        logging.debug("Tried get all patients but patients list is empty")
        return {"message": "Patient list is empty"}

    def post(self):
        """
        Get method for adding new patient to DB
        :return JSON message of success
        """
        new_patient = request.get_json(force=True)
        patient = patient_mapper.json_to_patient(new_patient)
        answer = patient_service.add_patient(patient)
        logging.debug("New patient was added to DB: %s", patient)
        return {"message": "Patient was added successfully",  "patient": json.loads(answer.to_json())}


class PatientAPIGetUpdateDelete(Resource):
    """
    Class for receiving GET and PUT DELETE methods with parameter id
    """

    def get(self, patient_id):
        """
        Get method for getting patient from DB by id
        :param patient_id:
        :return JSON Patient object:
        :except Patient was not found:
        """
        try:
            patient = patient_service.get_one_by_id(patient_id)
            logging.debug("Patient by id - %s was gotten, patient: %s", patient_id, patient)
            return json.loads(patient.to_json())
        except RuntimeError as error:
            logging.debug("Patient by id - %s was not found", patient_id)
            abort(404, str(error))

    def put(self, patient_id):
        """
        Put method for editing patient in DB by id
        :param patient_id:
        :return JSON Patient object:
        :except Patient was not found:
        """
        new_patient = request.get_json(force=True)
        patient = patient_mapper.json_to_patient(new_patient)
        try:
            patient_service.update(patient_id, patient)
            patient.patient_id = patient_id
            logging.debug("Patient by id - %s was updated, new patient: %s", patient_id, patient)
            return json.loads(patient.to_json())
        except RuntimeError as error:
            logging.debug("Patient for update by id - %s was not found", patient_id)
            abort(404, str(error))

    def delete(self, patient_id):
        """
        Put method for editing patient in DB by id
        :param patient_id:
        :return JSON Patient object:
        :except Patient was not found:
        """
        try:
            patient_service.delete(patient_id)
            logging.debug("Patient by id - %s was deleted", patient_id)
            return {"message": "Patient was successfully deleted"}
        except RuntimeError as error:
            logging.debug("Patient for delete by id - %s was not found", patient_id)
            abort(404, str(error))


api.add_resource(PatientAPIGetPost, '/patient-api')
api.add_resource(PatientAPIGetUpdateDelete, '/patient-api/<patient_id>')
