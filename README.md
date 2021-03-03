# protoapi

[dockerhub-badge]: https://img.shields.io/badge/images%20on-Docker%20Hub-blue.svg
[dockerhub-link]: https://hub.docker.com/repository/docker/virgesmith/protoapi

[![Docker Hub package][dockerhub-badge]][dockerhub-link]

docker/azure app service example, using flask and [open API](https://swagger.io/specification/) (f.k.a. swagger).

1. Expose a python package through a web API, using flask.
2. Document the API, using swagger.
3. Test the API, using pytest.
4. Package the web app, in a docker container.
5. Deploy the web app, in the cloud.
6. Automate!

A commit to master will set the ball rolling:

- docker hub will see the code changes and rebuild and test the image tagging it with 'latest'.
- azure will see a new image in docker hub and deploy it automatically.

## Steps

1. Fork this repo
2. Make changes as you see fit
3. Create a repository on e.g. docker hub
4. Point docker hub to your repo
5. Create a containerised app service on e.g. azure
6. Point your app service to docker hub, using a webhook
7. Commit your changes
8. Profit!

## Versioning

The script [release.py](./scripts/release.py) automates the process of creating and deploying a versioned (tagged) release.

In this case our version information is stored in [swagger.json](./static/swagger.json) using the [semantic versioning](https://semver.org/) format, i.e. `X.Y.Z`. The script increments the patch version (`Z`), commits the file, tags the repo with that version number, and pushes both the commit and the tag to master on `origin`.

Docker hub is configured to build both tags and the latest version of `master`, so will create two (identical) images, one with the version tag and one with the `latest` tag. The azure app service will deploy the `latest` tag (it doesn't seem easy to parameterise the tag, using a webhook at least).
