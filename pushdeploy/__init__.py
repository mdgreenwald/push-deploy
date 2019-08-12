import os
from flask import Flask, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_optional, create_access_token,
    get_jwt_identity
    )
from pushdeploy import apiv1

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')

    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def my_expired_token_callback(expired_token):
        token_type = expired_token['type']
        return jsonify({
            'status': 401,
            'sub_status': 42,
            'msg': 'The {} token has expired'.format(token_type)
        }), 401

    if test_config is None:
        app.config.from_pyfile("config.py", silent=False)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/health', methods=['GET'])
    @jwt_optional
    def health():
        return jsonify(
        status='healthy',
        releaseId='0.0.0',
        ), 200

    @app.route('/', methods=['GET'])
    @jwt_required
    def index():
        return jsonify(), 200

    app.register_blueprint(apiv1.bp)

    return app
