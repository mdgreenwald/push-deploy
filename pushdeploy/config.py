import os
basedir = os.path.abspath(os.path.dirname(__file__))

PD_REGISTRY = os.environ.get('PD_REGISTRY')
PD_USER = os.environ.get('PD_USER')
PD_PASSWORD = os.environ.get('PD_PASSWORD')
SECRET_KEY = os.environ.get('PD_SECRET_KEY')
