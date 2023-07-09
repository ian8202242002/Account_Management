from flask_restx import Api
from flask import Blueprint

from .user import api as user_ns

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, version='1.0', title='Account management API Swagger', description='account management')

api.add_namespace(user_ns)
