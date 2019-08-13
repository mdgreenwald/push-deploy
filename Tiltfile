# one static YAML file
k8s_yaml('./kubernetes/app.yaml')

docker_build('push-deploy', '.')

k8s_resource('push-deploy', port_forwards='5000:5000')
