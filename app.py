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



@app.route('/version', methods=["GET"])
def version():
  """ 
  Returns the version (git/docker tag)
  """
  try:
    with open("./static/swagger.json") as fp:
      return json.dumps(json.load(fp)["info"]["version"]), 200 
  except Exception as e:
    return { "code": 400, "name": e.__class__.__name__, "description": str(e) }, 400



@app.route('/sobol', methods=["GET"])
def sobol():
  """ 
  Returns a Sobol sequence
  """
  try:
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
    return json.dumps(hl.sobolSequence(dim, len).tolist()), 200 
  except Exception as e:
    return { "code": 400, "name": e.__class__.__name__, "description": str(e) }, 400


# e.g. [1.1,2.2,3.3,4.4]
@app.route('/integerise', methods=["POST"])
def integerise():
  """ 
  Returns the closest integer array to the supplied non-integer data, preserving the marginal sums
  """
  try:
    # json cant (de)serialise np.array
    array = np.array(json.loads(request.get_data())).astype(float)
    result = hl.integerise(array)
    if "result" in result:
      result["result"] = result["result"].tolist()
    return json.dumps(result), 200#, default_response_header
  except Exception as e:
    return { "code": 400, "name": e.__class__.__name__, "description": str(e) }, 400

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
