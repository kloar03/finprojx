from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from .config import Config

flask_app = Flask('finprojx', template_folder='app/templates')
flask_app.config.from_object(Config)

bootstrap = Bootstrap(flask_app)
CORS(flask_app)

from app import routes