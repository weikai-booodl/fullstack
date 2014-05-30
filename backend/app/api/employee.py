from flask_restful import Resource


class EmployeesResource(Resource):
    def get(self):
        return [dict(id=123, name="xwk")]

