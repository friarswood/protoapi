#Dockerfile

FROM ubuntu:20.04

LABEL Maintainer="Andrew Smith <andrew@friarswood.net>"
LABEL Description="Simple python flask app in a container"

RUN apt-get update && apt-get install -y python3.8 python3-pip

WORKDIR /app

COPY . /app

RUN python3.8 -m pip install -r requirements.txt

# default Flask port
EXPOSE 5000

# testing is standalone so can be run here (whilst there is no auth)
RUN pytest

# --host needs to be explicitly set here, not in the code, see
# https://stackoverflow.com/questions/30323224/deploying-a-minimal-flask-app-in-docker-server-connection-issues
CMD ["flask", "run", "--host", "0.0.0.0"]
