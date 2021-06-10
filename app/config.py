import os
from mongoengine import connect

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a very temporary secret key'
    MONGO = connect('finprojx_app', host='localhost', port=27017)
    DB = 'finprojx'