import os
from flask import Flask

def create_app(config_file):
    app = Flask(__name__, static_url_path='')
    app.config.from_pyfile(config_file)

    #If you need to override the default settings, create a customized
    # config file and set an environment variable as below
    # export FULLSTACK_CONFIG_FILE_PATH='/path/to/config/file'
    if os.environ.has_key("FULLSTACK_CONFIG_FILE_PATH"):
        app.config.from_envvar("FULLSTACK_CONFIG_FILE_PATH")

    from db import db
    db.init_app(app)

    from api import api_blueprint
    app.register_blueprint(api_blueprint)

    @app.route('/')
    def root():
        return app.send_static_file('index.html')

    return app