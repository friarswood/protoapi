# Dockerfile

FROM python

LABEL Maintainer="Andrew Smith <andrew@friarswood.net>"
LABEL Description="Simple python flask app in a container"

WORKDIR /app

COPY . /app

RUN pip install -U pip pytest gunicorn

# build, test
RUN pip install . && pytest

# clean up
RUN rm -rf .pytest_cache/ build/ test-appsvc.egg-info/ .eggs/

# default Flask port
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]