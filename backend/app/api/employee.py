import json
from flask import request
from flask_restful import Resource, abort, marshal_with, fields
from flask_login import current_user, login_required
from app.auth import api_login_required
from app.lib.utils import Paginator
from ..db import db, Employee, Department, Title, Salary


class DepartmentEmployeesResource(Resource):
    @api_login_required
    def get(self, dept_no):
        paginator = Paginator()
        department = Department.get_by_dept_no(dept_no)
        if not department:
            abort(404, message="No such department")

        if current_user.emp_rec.emp_no != department.current_manager.emp_no:
            abort(403, message="Only the manager can list all employees in a department")

        filters = json.loads(request.args.get("filters", "null"))

        employees = department.get_employees(offset=paginator.offset, limit=paginator.limit, filters=filters)
        return dict(employees = [employee.to_json() for employee in employees],
                    pagination_hint = paginator.get_pagination_hint(employees))

class EmployeeResource(Resource):

    @api_login_required
    def get(self, emp_no):
        employee = Employee.get_by_emp_no(emp_no)

        if not employee:
            abort(404, message="No such employee")

        if current_user.emp_rec.emp_no not in [emp_no, employee.current_department.current_manager.emp_no]:
            abort(403, message="Only the owner or the manager can access a employee's detail information")

        return employee.to_json()


