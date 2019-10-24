import functools
import json
from kubernetes import client, config
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

@bp.before_app_request
def init_api():
    """Creates instances of the incluster config and client API
    and stores them in global"""
    g.configuration = config.load_incluster_config()
    g.api_instance = client.AppsV1Api(client.ApiClient(g.configuration))
    g.PD_REGISTRY = current_app.config['PD_REGISTRY']

def read_deployment(deployment, namespace):
    namespace = "%s" % str(namespace)
    field = "metadata.name=%s" % str(deployment)
    api_response = g.api_instance.list_namespaced_deployment(
        namespace=namespace,
        field_selector=field
    )
    if len(api_response.items) == 1:
        return api_response.items[0]
    else:
        return "Deployment selector not unique enough."

def update_deployment(deployment_object, image_name, image_tag, deployment, namespace):
    image = "%s/%s:%s" % (g.PD_REGISTRY, image_name, image_tag)
    deployment_object.spec.template.spec.containers[0].image = image
    api_response = g.api_instance.patch_namespaced_deployment(
        name=deployment,
        namespace=namespace,
        body=deployment_object,
        field_manager="push-deploy")
    print("Deployment updated. status='%s'" % str(api_response.status))

@bp.route('/', methods=['GET'])
@jwt_required
def index():
    return jsonify(), 200

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
    access_token = create_access_token(identity=username, expires_delta=timedelta(seconds=90))
    return jsonify(access_token=access_token), 200

@bp.route('/deploy', methods=['GET'])
@jwt_required
def deploy():
    image_tag = request.args['image_tag']
    image_name = request.args['image_name']
    deployment = request.args['deployment']
    namespace = request.args['namespace']
    deploy = update_deployment(deployment_object=read_deployment(deployment=deployment, namespace=namespace), image_name=image_name, image_tag=image_tag, deployment=deployment, namespace=namespace)
    return jsonify(msg=deploy), 201
