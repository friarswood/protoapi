# protoapi

[dockerhub-badge]: https://img.shields.io/badge/images%20on-Docker%20Hub-blue.svg
[dockerhub-link]: https://hub.docker.com/repository/docker/virgesmith/protoapi 

[![Docker Hub package][dockerhub-badge]][dockerhub-link]

docker/azure app service example, using flask and [open API](https://swagger.io/specification/) (f.k.a. swagger).

See it in action [here](https://protocop.azurewebsites.net/api-doc)

1. Expose a python package as a web API, using flask.
2. Document the API, using swagger.
3. Test the API, using pytest.
3. Package the web app, in a docker container.
4. Deploy the web app, in the cloud.
5. Automate!

A commit to master will set the ball rolling:
- docker hub will see the code changes and rebuild and test the image.
- azure will see a new image in docker hub and deploy it automatically. 

# Steps

1. Fork this repo
2. Make changes as you see fit
3. Create a repository on e.g. docker hub
3. Point docker hub to your repo
5. Create a containerised app service on e.g. azure
4. Point your app service to docker hub, using a webhook
5. Commit your changes
6. Profit!