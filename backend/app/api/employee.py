from flask_restful import Resource, abort, marshal_with, fields
from flask_login import current_user, login_required
from ..db import db, Employee, Department, Title, Salary


class DepartmentEmployeesResource(Resource):
    @login_required
    def get(self, dept_no):
        """
        Notice dep_no is actually a string
        """
        department = Department.get_by_dept_no(dept_no)
        if not department:
            abort(404, message="No such department")

        if current_user.emp_rec.emp_no != department.current_manager.emp_no:
            abort(403, message="Only the manager can list all employees in a department")

        # return dict(employees=[{
        #     "emp_no": row.Employee.emp_no,
        #     "birth_date": str(row.Employee.birth_date),
        #     "first_name": row.Employee.first_name,
        #     "last_name": row.Employee.last_name,
        #     "gender": row.Employee.gender,
        #     "hire_date": str(row.Employee.hire_date),
        #     "current_department_name": row.Department.dept_name,
        #     "current_salary": row.Salary.salary,
        #     "current_title": row.Title.title,
        # } for row in department.employees])
        return dict(employees=[employee.to_json() for employee in department.employees])

class EmployeeResource(Resource):

    @login_required
    def get(self, emp_no):
        employee = Employee.get_by_emp_no(emp_no)

        if not employee:
            abort(404, message="No such employee")

        if current_user.emp_rec.emp_no not in [emp_no, employee.current_department.current_manager.emp_no]:
            abort(403, message="Only the owner or the manager can access a employee's detail information")

        return employee.to_json()


