from flask import Flask
from app.config import Config

app = Flask(__name__)
instance.config.from_object(Config)

