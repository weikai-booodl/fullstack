from flask import Blueprint
from flask.ext import restful
from employee import EmployeeResource, DepartmentEmployeesResource


api_blueprint = Blueprint('api', __name__)
api = restful.Api(api_blueprint, prefix="/api")

api.add_resource(EmployeeResource, '/employees/<int:emp_no>')
api.add_resource(DepartmentEmployeesResource, '/departments/<dept_no>/employees')
