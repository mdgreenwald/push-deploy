import os
basedir = os.path.abspath(os.path.dirname(__file__))

PD_NAMESPACE = os.environ.get('PD_NAMESPACE')
PD_DEPLOYMENT = os.environ.get('PD_DEPLOYMENT')
PD_USER = os.environ.get('PD_USER')
PD_PASSWORD = os.environ.get('PD_PASSWORD')
SECRET_KEY = os.environ.get('PD_SECRET_KEY')
