import json
import unittest
import sys
import math
from unit_test_helper import JsonTestCase, flask_app
import os

module_dir = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(module_dir, "..", ".."))
sys.path.append(project_dir)
from app.db import db, Employee, Department


module_dir = os.path.dirname(__file__)


class MyTest(JsonTestCase):
    def setUp(self):
        #make sure the user is logged out at the begining of each case
        self.json_http_request("post", 200, "/auth/logout")


    def test_current_custom_relationship_fields_of_employee(self):
        with flask_app.app_context():
            print "employee 499992 has worked for two departments, but the latest one is d001"
            emp = db.session.query(Employee).filter(Employee.emp_no == 499992).first()
            self.assertEqual(emp.current_department.dept_no, 'd001')

            print "employee 499992's current title should be senior staff"
            self.assertEqual(emp.current_title.title, 'Senior Staff')

            print "employee 499992's current salary should be 80389"
            self.assertEqual(emp.current_salary.salary, 80389)

            print "employee 499991 only worked for one department d009"
            emp = db.session.query(Employee).filter(Employee.emp_no == 499991).first()
            self.assertEqual(emp.current_department.dept_no, 'd009')

            print "employee 499991's current title should be Staff"
            self.assertEqual(emp.current_title.title, 'Staff')

            print "employee 499991's current salary should be 52867"
            self.assertEqual(emp.current_salary.salary, 52867)

    def test_manager_related_relationship_fields(self):
        with flask_app.app_context():
            print "employee 110039 is currently the manager of deparment d001"
            emp = db.session.query(Employee).filter(Employee.emp_no == 110039).first()
            self.assertEqual(emp.departments_currently_managing[0].dept_no, 'd001')
            self.assertEqual(emp.departments_currently_managing[0].current_manager, emp)

            print "employee 110022 is not manager of d001 any more"
            emp = db.session.query(Employee).filter(Employee.emp_no == 110022).first()
            self.assertEqual(emp.departments_currently_managing, [])

            print "employee 499992 has never been a manager"
            emp = db.session.query(Employee).filter(Employee.emp_no == 499992).first()
            self.assertEqual(emp.departments_currently_managing, [])

    def test_auth_api(self):
        print "access protected api should return 412"
        res = self.json_http_request("get", 412, "/api/departments/d001/employees")

        print "login with incorrect credential should get 412"
        res = self.json_http_request("post", 412, "/auth/login", data=dict(username="1234.1234", password="1234"))

        print "login with correct credential should get 200"
        res = self.json_http_request("post", 200, "/auth/login", data=dict(username="Georgi.Facello", password=10001))
        self.assertEqual(res.json["emp_no"], 10001)

        print "since employee 10001 is not a manager, the returend json should have empty departments_currently_managing"
        self.assertEqual(res.json["departments_currently_managing"], [])

        print "logout should return 200"
        res = self.json_http_request("post", 200, "/auth/logout")

        print "access protected api now should return 412"
        res = self.json_http_request("get", 412, "/api/departments/d001/employees")

        print "login as manager (110039) sould get a d001 as the only deparment he is managing"
        res = self.json_http_request("post", 200, "/auth/login", data=dict(username="Vishwani.Minakawa", password=110039))
        self.assertEqual(res.json["emp_no"], 110039)
        self.assertEqual(len(res.json["departments_currently_managing"]), 1)
        self.assertEqual(res.json["departments_currently_managing"][0]["dept_no"], "d001")


    def test_get_deparment_employees_api(self):
        print "login as a non-manager should not be able to acess any department's employee list API"
        res = self.json_http_request("post", 200, "/auth/login", data=dict(username="Georgi.Facello", password=10001))
        res = self.json_http_request("get", 403, "/api/departments/d005/employees")
        res = self.json_http_request("get", 403, "/api/departments/d001/employees")
        self.json_http_request("post", 200, "/auth/logout")

        print "login as manager of d001 should only be able to view this deparment's employee list but not others"
        res = self.json_http_request("post", 200, "/auth/login", data=dict(username="Vishwani.Minakawa", password=110039))
        res = self.json_http_request("get", 403, "/api/departments/d005/employees")

        res = self.json_http_request("get", 200, "/api/departments/d001/employees?limit=-1")   #disable the default pagination

        print "department d001 should have 14842 employees currently"
        self.assertEqual(len(res.json["employees"]), 14842)

        print "department d001's current employee should include 499992"
        self.assertTrue(499992 in [employee["emp_no"] for employee in res.json["employees"]])

        print "department d001's current employee should not include 499991"
        self.assertTrue(499991 not in [employee["emp_no"] for employee in res.json["employees"]])

        print "By default, the pagination mechanism will only return the first 20 results"
        res = self.json_http_request("get", 200, "/api/departments/d001/employees")
        self.assertEqual(len(res.json["employees"]), 20)

        print "the result should have no previous page"
        self.assertTrue("prev_page" not in res.json["pagination_hint"])

        print "the result should have next page"
        self.assertTrue("next_page" in res.json["pagination_hint"])

        # print "total should be", 14842
        # self.assertEqual(res.json["pagination_hint"]["total"], 14842)

        last_employee_of_first_page = res.json["employees"][-1]

        print "follow the next_page url", res.json["pagination_hint"]["next_page"]["url"]

        #in testing app, we have to taken out the http://host portion. otherwise the behavior is strange in
        #that the query string will be stripped off
        url = res.json["pagination_hint"]["next_page"]["url"].split("/", 3)[-1]
        res = self.json_http_request("get", 200, url)
        self.assertEqual(len(res.json["employees"]), 20)

        print "second page should have both next_page and previous_page"
        print res.json

        self.assertTrue("next_page" in res.json["pagination_hint"])
        self.assertTrue("prev_page" in res.json["pagination_hint"])

        print "the first person in the 2nd page should have higher emp_no than the last person in the first page"
        first_employee_of_2nd_page = res.json["employees"][0]

        self.assertGreater(first_employee_of_2nd_page["emp_no"], last_employee_of_first_page["emp_no"])

        print "request 10 rows from offset 20"
        res = self.json_http_request("get", 200, "/api/departments/d001/employees?limit=10&offset=20")
        self.assertEqual(len(res.json["employees"]), 10)

        print "no matter how many items in a page, the offset 20 should return the same person"
        first_employee_of_this_page = res.json["employees"][0]
        self.assertEqual(first_employee_of_2nd_page["emp_no"], first_employee_of_this_page["emp_no"])

        print "try to request beyond the range should get empty result"
        res = self.json_http_request("get", 200, "/api/departments/d001/employees?limit=40&offset=200000")
        self.assertEqual(len(res.json["employees"]), 0)

        print "try to retrieve only employees whose first name contains 'risti' in d001 (there is at least one)"
        res = self.json_http_request("get", 200, "/api/departments/d001/employees?filters=%s" %
            json.dumps(dict(first_name="risti")))

        self.assertGreater(len(res.json["employees"]), 0)
        for employee in res.json["employees"]:
            self.assertTrue(employee["first_name"].find("risti")>=0)

        print "try to search exact firstanem Genki in dept 001"
        res = self.json_http_request("get", 200, "/api/departments/d001/employees?filters=%s" %
            json.dumps(dict(first_name="Genki")))

        self.assertGreater(len(res.json["employees"]), 0)
        print res.json

    #
    # def test_get_employee_api(self):
    #     res = self.json_http_request("get", 200, "/api/employees/499992")
    #     self.assertEqual(res.json["emp_no"], 499992)
    #     self.assertEqual(res.json["first_name"], "Siamak")
    #     self.assertEqual(res.json["last_name"], "Salverda")
    #     self.assertEqual(res.json["gender"], "F")
    #     self.assertEqual(res.json["current_department_name"], "Marketing")
    #     self.assertEqual(res.json["current_salary"], 80389)
    #     self.assertEqual(res.json["current_title"], "Senior Staff")


if __name__ == '__main__':
    unittest.main()

