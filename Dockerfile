# Dockerfile
# TODO this installs directly from the dev env, which means lots of clutter
# Ideally, this image should be created from a package, but this changes the workflow:
# rather than (as now) docker hub building an image from the source tree (whenever it changes),
# CI should create a package, and then use it to build an image and push to docker hub

FROM python

LABEL Maintainer="Andrew Smith <andrew@friarswood.net>"
LABEL Description="Simple python flask app in a container"

WORKDIR /app

COPY . /app

RUN pip install -U pip pytest gunicorn

# build, test
RUN pip install -e . && pytest

# clean up
RUN rm -rf .pytest_cache/ build/ test-appsvc.egg-info/ .eggs/

# default Flask port
EXPOSE 5000

# --host needs to be explicitly set here, not in the code, see
# https://stackoverflow.com/questions/30323224/deploying-a-minimal-flask-app-in-docker-server-connection-issues
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]