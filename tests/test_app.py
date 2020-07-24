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

def test_version(client):

  response = client.get(url("version"))
  assert response.status_code == 200
  result = json.loads(response.data)
  assert len(result.split(".")) == 3


def test_sobol(client):

  response = client.get(url("sobol"))
  assert response.status_code == 400
  result = json.loads(response.data)
  assert result["code"] == 400

  # invalid dim
  result = json.loads(client.get(url("sobol", {"dimension": 0, "length": 2})).data)
  assert result["code"] == 400
  result = json.loads(client.get(url("sobol", {"dimension": 2000, "length": 2})).data)
  assert result["code"] == 400
  result = json.loads(client.get(url("sobol", {"dimension": "x", "length": 2})).data)
  assert result["code"] == 400

  result = json.loads(client.get(url("sobol", {"dimension": 2, "length": 2})).data)
  assert isinstance(result, list)
  assert len(result) > 0
  assert isinstance(result[0], list)
  assert len(result[0]) > 0


def test_integerise(client):
  input = [1.1, 2.2, 3.3, 4.4]
  result = json.loads(client.post(url("integerise"), data=json.dumps(input)).data)
  assert isinstance(result, dict)
  assert "result" in result
  assert "rmse" in result
  assert "conv" in result 
  assert result["conv"]

  input = [[ 0.3,  1.2,  2.0, 1.5],
           [ 0.6,  2.4,  4.0, 3.0],
           [ 1.5,  6.0, 10.0, 7.5],
           [ 0.6,  2.4,  4.0, 3.0]]
  result = json.loads(client.post(url("integerise"), data=json.dumps(input)).data)
  assert isinstance(result, dict)
  assert "result" in result
  assert "rmse" in result
  assert "conv" in result 
  assert result["conv"]


if __name__ == "__main__":
  unittest.main()
