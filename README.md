# protoapi

docker/azure app service example, using flask and swagger.

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