#!/usr/bin/env python3

import os
from flask import Flask, request
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
import numpy as np
import json
import sys

SWAGGER_URL = '/api-doc'  # URL for exposing Swagger UI (without trailing '/')
# Our API url (can of course be a local resource)
API_URL = '/static/swagger.json'

app = Flask(__name__)
app.debug = True

import humanleague as hl


@app.route('/sobol', methods=["GET"])
def sobol():
  """ 
  Returns force boundary data
  """
  try:
    return json.dumps(hl.sobolSequence(int(request.args["dimension"]), int(request.args["length"])).tolist()), 200 #, default_response_header
  except Exception as e:
    return { "code": 400, "name": e.__class__.__name__, "description": str(e) }, 400#, default_response_header


# e.g. [1.1,2.2,3.3,4.4]
@app.route('/integerise', methods=["POST"])
def integerise():
  """ 
  Returns the closest integer array to the supplied non-integer data, preserving the marginal sums
  """
  try:
    # json cant (de)serialise np.array
    array = np.array(json.loads(request.get_data()))
    result = hl.integerise(array)
    if "result" in result:
      result["result"] = result["result"].tolist()
    return json.dumps(result), 200#, default_response_header
  except Exception as e:
    return { "code": 400, "name": e.__class__.__name__, "description": str(e) }, 400#, default_response_header

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
  SWAGGER_URL, # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
  API_URL,
  config = { 
    'app_name': "Prototype Data Service"
  }
)

# Register blueprint at URL
# (URL must match the one given to factory function above)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
  app.run()
