from flask import Flask

flask_app = Flask('finprojx', template_folder='app/templates')

from app import routes
