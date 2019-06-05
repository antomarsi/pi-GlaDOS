from flask_restplus import Api
from flask import Blueprint

from .cats import api as ns1

blueprint = Blueprint('api', __name__, url_prefix='/api/1')
api = Api(
    blueprint,
    title='Glados API',
    version='1.0',
    description='Basic Glados API',
)

api.add_namespace(ns1, path="/cat")