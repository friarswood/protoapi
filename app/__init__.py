
import os
from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException
import numpy as np
import json
import humanleague as hl
import logging

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_app(test_config=None):

  SWAGGER_URL = ''  # URL for exposing Swagger UI (without trailing '/')
  # Our API url (can of course be a local resource)
  API_URL = '/static/swagger.json'

  app = Flask(__name__, instance_relative_config=True)

  # if we have an app insights key, redirect logging to it
  if "APPINSIGHTS_INSTRUMENTATIONKEY" in os.environ:
    # See https://docs.microsoft.com/en-us/azure/azure-monitor/app/opencensus-python-request
    # and https://docs.microsoft.com/en-us/azure/azure-monitor/app/asp-net-trace-logs

    from opencensus.ext.azure.log_exporter import AzureLogHandler
    # from opencensus.ext.azure.trace_exporter import AzureExporter
    # from opencensus.ext.flask.flask_middleware import FlaskMiddleware
    # from opencensus.trace.samplers import ProbabilitySampler

    connection_string = f'InstrumentationKey={os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")};IngestionEndpoint=https://uksouth-1.in.applicationinsights.azure.com/'
    logger.addHandler(AzureLogHandler(connection_string=connection_string))

    # middleware = FlaskMiddleware(
    #   app,
    #   exporter=AzureExporter(connection_string=f'InstrumentationKey={os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")}'),
    #   sampler=ProbabilitySampler(rate=1.0),
    # )

  app.config.from_mapping(SECRET_KEY='TODO dev')

  @app.route('/headers', methods=["GET"])
  def headers():
    """
    Returns the https headers of the request
    """
    logger.info("header")
    return json.dumps({k: v for k, v in request.headers})


  @app.route('/sobol', methods=["GET"])
  def sobol():
    """
    Returns a Sobol sequence
    """
    # deferring to swagger/schema for validity means that
    # - the schema must "know" the validity ranges of the arguments to sobolSequence
    # - the function itself may be better at providing a meaningful error message
    # - passing invalid values to the API directly will still fail, and possibly badly
    dim = int(request.args["dimension"])
    if dim < 1 or dim > 1111:
      raise ValueError("Sobol dimension %d is outside the valid range [1,1111]" % dim)
    len = int(request.args["length"])
    if len < 1 or len > 1048576:
      raise ValueError("Sobol sequence length %d is outside the valid range [1,1048576]" % len)
    logger.info(f"sobol {dim} x {len}")
    return json.dumps(hl.sobolSequence(dim, len).tolist())


  # e.g. [1.1,2.2,3.3,4.4]
  @app.route('/integerise', methods=["POST"])
  def integerise():
    """
    Returns the closest integer array to the supplied non-integer data (with integer marginal sums), preserving the marginal sums
    """
    # json cant (de)serialise np.array
    array = np.array(json.loads(request.get_data())).astype(float)
    result = hl.integerise(array)
    # if a string throw it
    if isinstance(result, str):
      raise ValueError(result)
    if isinstance(result, dict) and "result" in result:
      result["result"] = result["result"].tolist()
      logger.info("integerise")
      return json.dumps(result)

  @app.errorhandler(Exception)
  def handle_exception(e):
    logger.exception(e)
    # pass through HTTP errors
    if isinstance(e, HTTPException):
      return e
    # handle non-HTTP exceptions
    return { "type": e.__class__.__name__, "description": str(e) }, 500

  # Call factory function to create our blueprint
  swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config = {
      'app_name': "Test App Service"
    }
  )

  # Register blueprint at URL
  # (URL must match the one given to factory function above)
  app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

  return app

# if __name__ == '__main__':
#   app.run()
