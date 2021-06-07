from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config

flask_app = Flask('finprojx', template_folder='app/templates')
flask_app.config.from_object(Config)

bootstrap = Bootstrap(flask_app)

# from app import central
from app.routes import (
    add,
    add_account,
    add_event,
    data,
    drop,
    home,
    schedule,
    simulate,
)