import os
from werkzeug.middleware.proxy_fix import ProxyFix
from pushdeploy import create_app

app = ProxyFix(create_app(), x_for=1, x_host=1)