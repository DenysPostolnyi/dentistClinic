"""
Init for views
"""
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

main = Blueprint('main', __name__)


@main.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)
