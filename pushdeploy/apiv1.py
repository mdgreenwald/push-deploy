import functools
import json
from kubernetes import client, config
from datetime import timedelta
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for, jsonify
from flask_jwt_extended import JWTManager, jwt_required, jwt_optional, create_access_token, get_jwt_identity

bp = Blueprint("apiv1", __name__, url_prefix="/api/v1")

@bp.before_app_request
def init_api():
    """Creates instances of the incluster config and client API
    and stores them in global"""
    g.configuration = config.load_incluster_config()
    g.apps_v1_api_instance = client.AppsV1Api(client.ApiClient(g.configuration))
    g.batch_v1beta1_instance = client.BatchV1beta1Api(client.ApiClient(g.configuration))
    g.PD_REGISTRY = current_app.config['PD_REGISTRY']

def list_cron_job(name, namespace):
    namespace = "%s" % str(namespace)
    name = "metadata.name=%s" % str(name)
    api_response = g.batch_v1beta1_instance.list_namespaced_cron_job(
        namespace=namespace,
        field_selector=name
    )
    if len(api_response.items) == 1:
        return api_response.items[0]
    else:
        return "CronJob selector not unique enough."

def list_daemon_set(name, namespace):
    namespace = "%s" % str(namespace)
    name = "metadata.name=%s" % str(name)
    api_response = g.apps_v1_api_instance.list_namespaced_daemon_set(
        namespace=namespace,
        field_selector=name
    )
    if len(api_response.items) == 1:
        return api_response.items[0]
    else:
        return "DaemonSet selector not unique enough."

def list_deployment(name, namespace):
    namespace = "%s" % str(namespace)
    name = "metadata.name=%s" % str(name)
    api_response = g.apps_v1_api_instance.list_namespaced_deployment(
        namespace=namespace,
        field_selector=name
    )
    if len(api_response.items) == 1:
        return api_response.items[0]
    else:
        return "Deployment selector not unique enough."

def patch_cron_job(cron_job_object, image_name, image_tag, name, namespace):
    image = "%s/%s:%s" % (g.PD_REGISTRY, image_name, image_tag)
    cron_job_object.spec.job_template.spec.template.spec.containers[0].image = image
    api_response = g.batch_v1beta1_instance.patch_namespaced_cron_job(
        name=name,
        namespace=namespace,
        body=cron_job_object,
        field_manager="push-deploy")
    print("CronJob updated. status='%s'" % str(api_response.status))

def patch_daemon_set(daemon_set_object, image_name, image_tag, name, namespace):
    image = "%s/%s:%s" % (g.PD_REGISTRY, image_name, image_tag)
    daemon_set_object.spec.template.spec.containers[0].image = image
    api_response = g.apps_v1_api_instance.patch_namespaced_daemon_set(
        name=name,
        namespace=namespace,
        body=daemon_set_object,
        field_manager="push-deploy")
    print("DaemonSet updated. status='%s'" % str(api_response.status))

def patch_deployment(deployment_object, image_name, image_tag, name, namespace):
    image = "%s/%s:%s" % (g.PD_REGISTRY, image_name, image_tag)
    deployment_object.spec.template.spec.containers[0].image = image
    api_response = g.apps_v1_api_instance.patch_namespaced_deployment(
        name=name,
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

@bp.route('/cronjob', methods=['POST'])
@jwt_required
def cronjob():
    image_tag = request.args['image_tag']
    image_name = request.args['image_name']
    name = request.args['name']
    namespace = request.args['namespace']
    cronjob = patch_cron_job(
        cron_job_object=list_cron_job(name=name, namespace=namespace),
        image_name=image_name,
        image_tag=image_tag,
        name=name,
        namespace=namespace)
    return jsonify(msg=cronjob), 201

@bp.route('/daemonset', methods=['POST'])
@jwt_required
def daemonset():
    image_tag = request.args['image_tag']
    image_name = request.args['image_name']
    name = request.args['name']
    namespace = request.args['namespace']
    daemonset = patch_daemon_set(
        daemon_set_object=list_daemon_set(name=name, namespace=namespace),
        image_name=image_name,
        image_tag=image_tag,
        name=name,
        namespace=namespace)
    return jsonify(msg=daemonset), 201

@bp.route('/deploy', methods=['GET'])
@jwt_required
def deploy():
    image_tag = request.args['image_tag']
    image_name = request.args['image_name']
    name = request.args['deployment']
    namespace = request.args['namespace']
    deploy = patch_deployment(
        deployment_object=list_deployment(name=name, namespace=namespace),
        image_name=image_name,
        image_tag=image_tag,
        name=name,
        namespace=namespace)
    return jsonify(msg=deploy), 201

@bp.route('/deployment', methods=['POST'])
@jwt_required
def deployment():
    image_tag = request.args['image_tag']
    image_name = request.args['image_name']
    name = request.args['name']
    namespace = request.args['namespace']
    deployment = patch_deployment(
        deployment_object=list_deployment(name=name, namespace=namespace),
        image_name=image_name,
        image_tag=image_tag,
        name=name,
        namespace=namespace)
    return jsonify(msg=deployment), 201
