from flask import Blueprint
from flask.ext import restful
from employee import EmployeesResource


api_blueprint = Blueprint('api', __name__)
api = restful.Api(api_blueprint, prefix="/api")
api.add_resource(EmployeesResource, '/employees')