"""
Tests
"""

import pytest
import json
#import unittest
from urllib.parse import urlencode
from math import isclose
import requests

import sys
sys.path.append('.')
from app import app 

@pytest.fixture
def client():
  return app.test_client()

def url(endpoint, query_params = None):
  if query_params is None:
    return "/%s" % endpoint
  return "/%s?%s" % (endpoint, urlencode(query_params))

def test_sobol(client):

  result = json.loads(client.get(url("sobol")).data)
  assert result["code"] == 400

  result = json.loads(client.get(url("sobol", {"dimension": 2, "length": 2})).data)
  #assert result == True

  # result = json.loads(client.get(url("isbusinessday", {"date": "2020-03-08", "centre": "LON"})).data)
  # assert result == False


def test_integerise(client):
  input = [1.1, 2.2, 3.3, 4.4]
  result = json.loads(client.post(url("integerise"), data=json.dumps(input)).data)
  assert "result" in result
  assert "rmse" in result
  assert "conv" in result 
  assert result["conv"]

  input = [[ 0.3,  1.2,  2.0, 1.5],
           [ 0.6,  2.4,  4.0, 3.0],
           [ 1.5,  6.0, 10.0, 7.5],
           [ 0.6,  2.4,  4.0, 3.0]]
  result = json.loads(client.post(url("integerise"), data=json.dumps(input)).data)
  assert "result" in result
  assert "rmse" in result
  assert "conv" in result 
  assert result["conv"]


if __name__ == "__main__":
  unittest.main()
