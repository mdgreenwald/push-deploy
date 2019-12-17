# Push-Deploy

Push-Deploy is a Python application which helps to securely and simply enable communication between external tools (GitHub Actions, Circle CI, etc…) and Kubernetes without exposing cluster credentials. Instead it exposes an API which accepts parameters.

Push-deploy is focused on projects which may not have `semver` in place where other tools like [keel.sh](https://keel.sh/) and [weave/flux](https://github.com/fluxcd/flux) would make more sense.

--

## Disclaimer

This is pre-release software and is very limited. It will have bugs and lacks many features planned for later releases. The API may also change in ways which are not backwards compatible.

## Configuration

* `PD_REGISTRY`: Registry URI e.g. `258640715359.dkr.ecr.us-west-2.amazonaws.com`
* `PD_SECRET_KEY`: A very long (64+ Char) Alpha Numeric string
* `PD_USER`: Username to authenticate with
* `PD_PASSWORD`: Password to authenticate with

## Usage

```bash
TOKEN=$(
    curl -H "Content-Type: application/json" -X POST \
    -d '{"username":"service_account_name","password":"as8djareallylongstring9asdj8a8sdj"}' \
    http://pushdeploy.domain.com/api/v1/auth
    )
```

```bash
curl -H "Authorization: Bearer $TOKEN" \
http://pushdeploy.domain.com/api/v1/deploy?image_name=my_image&image_tag=v1.0.3
```

## Contributing

#### Dependencies

**Note:** push-deploy uses `config.load_incluster_config()`and depends on the kubernetes api and thus cannot be meaningfuly run outside of a cluster.

- Local Docker Daemon

- Kubernetes Cluster (Remote or local e.g. Docker for Mac Kubernetes, Microk8s, Minikube, etc...)

- [Tilt](https://tilt.dev/)

#### Resources

- [kubernetes-client/python](https://github.com/kubernetes-client/python)

- [flask](https://flask.palletsprojects.com/)

- [gunicorn](https://gunicorn.org/)

#### Usage

From root:

```bash
$ tilt up
```

Tilt will now continuously monitor for changes and rebuild and re-apply.
