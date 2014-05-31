import unittest
import random
import os
import sys
import json
module_dir = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(module_dir, "..", ".."))
sys.path.append(project_dir)
from run import app as flask_app


class JsonTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        flask_app.debug = True
        cls.app_client = flask_app.test_client()

    @classmethod
    def createRandomString(cls, length=10):
        return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for x in range(length))

    @classmethod
    def json_http_request(cls, method, expected_code, url, data=None, *args, **kwargs):
        """
        A helper for testin json api
        1) it sets content-type properly
        2) it add a res.json field if the result is in valid json
        3) it will print out the response data if the returned statu code is not the same as expected
        """
        method_name = method.lower()
        func = getattr(cls.app_client, method_name)
        res = func(url, data=json.dumps(data) if data else None, content_type='application/json', *args, **kwargs)
        if res.status_code != expected_code:
            print res.status_code, res.data
            raise AssertionError("%d != %d" % (res.status_code, expected_code))
        else:
            try:
                res.json = json.loads(res.data)
            except:
                pass
            return res
