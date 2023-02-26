import json

from flask import abort, Flask, Blueprint, request
from flask_restful import Resource, Api
from src.service import patient_service
from src.util import patient_mapper

app = Flask(__name__)
api_patient = Blueprint('patient_api', __name__)
api = Api(api_patient)


class PatientAPIGetPost(Resource):
    def get(self):
        patients = patient_service.get_all()
        if patients:
            return [json.loads(obj.to_json()) for obj in patients]
        else:
            abort(404, "Patients were not found")

    def post(self):
        new_patient = request.get_json(force=True)
        patient = patient_mapper.json_to_patient(new_patient)
        patient_service.add_patient(patient)
        return {"message": "Patient was added successfully"}


class PatientAPIGetUpdateDelete(Resource):
    def get(self, id):
        try:
            patient = patient_service.get_one_by_id(id)
            return json.loads(patient.to_json())
        except RuntimeError as error:
            abort(404, error)

    def put(self, id):
        new_patient = request.get_json(force=True)
        patient = patient_mapper.json_to_patient(new_patient)
        try:
            patient_service.update(id, patient)
            patient.patient_id = id
            return json.loads(patient.to_json())
        except RuntimeError as error:
            abort(404, str(error))

    def delete(self, id):
        try:
            patient_service.delete(id)
            return {"message": "Patient was successfully deleted"}
        except RuntimeError as error:
            abort(404, str(error))


api.add_resource(PatientAPIGetPost, '/patient-api')
api.add_resource(PatientAPIGetUpdateDelete, '/patient-api/<id>')
