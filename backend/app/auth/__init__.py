from flask import Blueprint
from flask.ext import restful

from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_restful import Resource, reqparse, abort
from app.db import Employee
from functools import wraps


login_manager = LoginManager()

def auth_init(app):
    login_manager.init_app(app)
    app.register_blueprint(auth_blueprint)


class LoginUserMixin(UserMixin):
    def __init__(self, emp_rec):
        self.emp_rec = emp_rec

    def get_id(self):
        return str(self.emp_rec.emp_no)

@login_manager.user_loader
def load_user(emp_no):
    emp_rec = Employee.get_by_emp_no(emp_no)
    return None if emp_rec is None else LoginUserMixin(emp_rec)


auth_blueprint = Blueprint('auth', __name__)
auth_api = restful.Api(auth_blueprint, prefix="/auth")

login_arg_parser = reqparse.RequestParser()
login_arg_parser.add_argument('username', type=str, required=True)
login_arg_parser.add_argument('password', type=str, required=True)

class LoginResource(Resource):
    def post(self):
        args = login_arg_parser.parse_args()
        first_name, sep, last_name = args["username"].partition('.')
        if not first_name or not last_name:
            abort(400, message="Invalid username format. Username is like firstname.lastname")

        employee = Employee.get_by_emp_no(args["password"])
        if employee and employee.first_name==first_name and employee.last_name==last_name:
            login_user(LoginUserMixin(employee))
        else:
            abort(412, message="Invalid username and password combination")  #401 will cause the browser to pop up its login dialog

        return dict(emp_no=employee.emp_no,
                    first_name=employee.first_name,
                    departments_currently_managing=[dict(dept_name=dept.dept_name, dept_no=dept.dept_no)
                                                for dept in employee.departments_currently_managing]
            ), 200

class LogoutResource(Resource):
    def post(self):
        logout_user()
        return "", 200

auth_api.add_resource(LoginResource, '/login')
auth_api.add_resource(LogoutResource, '/logout')




def api_login_required(message=None, admin_required=False):
    """
    Method decorator.
    Ensures the requesting user is authenticated.
    Otherwise a 412 is raised with an optional message.

    The default flask-login.login_required does not allow customized status code nor json-message

    Usage:
    @api_login_required

    Or:
    @api_login_required(message='You need to be logged in to blah.')
    """
    if callable(message):
        func = message
        decorator = api_login_required()
        return decorator(func)

    def decorator(func):

        def inner(*args, **kwargs):
            if not current_user.is_authenticated():
                abort_kwargs = {} if message is None else {'message': message}
                abort(412, **abort_kwargs)

            return func(*args, **kwargs)

        return wraps(func)(inner)

    return decorator


