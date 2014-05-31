from flask.ext.sqlalchemy import SQLAlchemy
import math
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import Session
from sqlalchemy import and_, ForeignKey
from datetime import datetime
from ..lib.utils import today

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % self.username

class Department(db.Model):
    __tablename__ = "departments"

    dept_no = db.Column(db.String(4), primary_key=True)
    dept_name = db.Column(db.String(40), unique=True)

    @classmethod
    def get_by_dept_no(cls, dept_no):
        return db.session.query(Department).filter(Department.dept_no == dept_no).first()

    @property
    def employees(self):
        # res = db.session.query(Department, Employee, Salary, Title)\
        #                 .join(DeptEmployee, and_(DeptEmployee.dept_no == Department.dept_no,
        #                                          DeptEmployee.to_date > today()))\
        #                 .join(Employee, Employee.emp_no == DeptEmployee.emp_no)\
        #                 .join(Salary, and_(Salary.emp_no == Employee.emp_no,
        #                                     Salary.to_date > today()))\
        #                 .join(Title, and_(Title.emp_no == Employee.emp_no,
        #                                     Title.to_date > today()))\
        #                 .filter(Department.dept_no == self.dept_no)\
        #                 .order_by(Employee.first_name)
        res = db.session.query(Employee).filter(Department.dept_no == self.dept_no,
                                                DeptEmployee.dept_no == Department.dept_no,
                                                DeptEmployee.to_date > today(),
                                                Employee.emp_no == DeptEmployee.emp_no)
        return res


class DeptEmployee(db.Model):
    __tablename__ = "dept_emp"

    emp_no = db.Column(db.Integer, ForeignKey('employees.emp_no'), primary_key=True)
    dept_no = db.Column(db.String(4), ForeignKey('departments.dept_no'), primary_key=True)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)


class DeptManager(db.Model):
    __tablename__ = "dept_manager"

    emp_no = db.Column(db.Integer, ForeignKey('employees.emp_no'), primary_key=True)
    dept_no = db.Column(db.String(4), ForeignKey('departments.dept_no'), primary_key=True)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)


class Salary(db.Model):
    __tablename__ = "salaries"

    emp_no = db.Column(db.Integer, ForeignKey('employees.emp_no'), primary_key=True)
    salary = db.Column(db.Integer)
    from_date = db.Column(db.Date, primary_key=True)
    to_date = db.Column(db.Date)


class Title(db.Model):
    __tablename__ = "titles"

    emp_no = db.Column(db.Integer, ForeignKey('employees.emp_no'), primary_key=True)
    title = db.Column(db.String(50), primary_key=True)
    from_date = db.Column(db.Date, primary_key=True)
    to_date = db.Column(db.Date, nullable=True)


class Employee(db.Model):
    __tablename__ = "employees"

    emp_no = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.Date)
    first_name = db.Column(db.String(14))
    last_name = db.Column(db.String(16))
    gender = db.Column(db.Enum("M", "F"))
    hire_date = db.Column(db.Date)


    current_department = relationship(Department,
                                      primaryjoin=and_(
                                        DeptEmployee.emp_no == emp_no,
                                        DeptEmployee.to_date > today(),  # some employees have transfered between departments
                                        ),
                                      secondaryjoin= (DeptEmployee.dept_no == Department.dept_no),
                                      secondary='dept_emp',
                                      uselist=False,
                                      viewonly=True,
                                      lazy="joined",    #use join-based eager loading to reduce SQL query to server
                                    )

    current_title = relationship(Title,
                                      primaryjoin=and_(
                                        Title.emp_no == emp_no,
                                        Title.to_date > today(),  # some employees have transfered between departments
                                        ),
                                      uselist=False,
                                      viewonly=True,
                                      lazy="joined"    #use join-based eager loading to reduce SQL query to server
                                    )

    current_salary = relationship(Salary,
                                      primaryjoin=and_(
                                        Salary.emp_no == emp_no,
                                        Salary.to_date > today(),  # some employees have transfered between departments
                                        ),
                                      uselist=False,
                                      viewonly=True,
                                      lazy="joined"    #use join-based eager loading to reduce SQL query to server
                                    )

    departments_currently_managing = relationship(Department,
                                      primaryjoin=and_(
                                        DeptManager.emp_no == emp_no,
                                        DeptManager.to_date > today(),  # some employees have transfered between departments
                                        ),
                                      secondaryjoin= (DeptManager.dept_no == Department.dept_no),
                                      secondary='dept_manager',
                                      viewonly=True,
                                      lazy="joined",    #use join-based eager loading to reduce SQL query to server
                                      backref=backref('current_manager', uselist=False)
                                    )


    # @property
    # def department_currently_managing(self):
    #     session = Session.object_session(self)
    #     return session.query(Department).filter(DeptManager.emp_no == self.emp_no,
    #                                             DeptManager.to_date > today(),
    #                                             Department.dept_no == DeptManager.dept_no).first()

    @classmethod
    def get_by_emp_no(cls, emp_no):
        return db.session.query(Employee).filter(Employee.emp_no == emp_no).first()

    def to_json(self):
        return {
            "emp_no": self.emp_no,
            "birth_date": str(self.birth_date),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "hire_date": str(self.hire_date),
            "current_department_name": self.current_department.dept_name,
            "current_salary": self.current_salary.salary,
            "current_title": self.current_title.title,
            }        