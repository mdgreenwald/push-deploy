import functools

from datetime import timedelta
from flask import Blueprint
from flask import current_app
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import jsonify

from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_optional, create_access_token,
    get_jwt_identity
    )

bp = Blueprint("apiv1", __name__, url_prefix="/api/v1")

@bp.route('/auth', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != current_app.config['PD_USER'] or password != current_app.config['PD_PASSWORD']:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username, expires_delta=timedelta(seconds=300))
    return jsonify(access_token=access_token), 200

@bp.route('/', methods=['GET'])
@jwt_required
def index():
    return jsonify(), 200
    
@bp.route('/deploy', methods=['GET'])
@jwt_required
def deploy():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
