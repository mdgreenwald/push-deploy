# Push-Deploy #

Push-Deploy is a Python application which helps to securely and simply enable communication between external tools (GitHub Actions, Circle CI, etc…) and Kubernetes without exposing cluster credentials.

In particular for projects which may not have `semver` inplace where other tools like [keel.sh](https://keel.sh/) and [weave/flux](https://github.com/fluxcd/flux) would make more sense.

--

### Disclaimer ###

This is pre-release software and is very limited. It will have bugs and lacks many features planned for later releases. The API may also change in ways which are not backwards compatible.

### Configuration ###

* `PD_NAMESPACE`: Namespace of the deployment
* `PD_DEPLOYMENT`: Name of the deployment
* `PD_REGISTRY`: Registry URI e.g. `258640715359.dkr.ecr.us-west-2.amazonaws.com`
* `PD_SECRET_KEY`: A very long (64+ Char) Alpha Numeric string
* `PD_USER`: Username to authenticate with
* `PD_PASSWORD`: Password to authenticate with

### Usage ###

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