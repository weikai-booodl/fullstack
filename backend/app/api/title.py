import json
from flask import request
from flask_restful import Resource, abort, marshal_with, fields
from flask_login import current_user, login_required
from app.auth import api_login_required
from app.lib.utils import Paginator
from ..db import db, Employee, Department, Title, Salary



class TitlesResource(Resource):

    @api_login_required
    def get(self):
        """
        return: all titles in the db
        """
        return dict(titles=[row.title for row in db.session.query(Title.title).distinct()])




