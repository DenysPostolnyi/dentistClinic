"""
Routes for testing DB services
"""
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
doctor_routes = Blueprint('doctor_routes', __name__,
                             template_folder='templates')


@doctor_routes.route('/doctors')
def index():
    try:
        return render_template('doctors.html')
    except TemplateNotFound:
        abort(404)
