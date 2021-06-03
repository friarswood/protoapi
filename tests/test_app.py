"""
Tests
"""

import pytest
import json
import unittest
from urllib.parse import urlencode
from math import isclose

import app

@pytest.fixture
def protoapi():
  protoapi = app.create_app({"TESTING": True})
  yield protoapi

@pytest.fixture
def client(protoapi):
  return protoapi.test_client()


def url(endpoint, query_params = None):
  if query_params is None:
    return "/%s" % endpoint
  return "/%s?%s" % (endpoint, urlencode(query_params))

def test_headers(client):

  response = client.get(url("headers"))
  assert response.status_code == 200
  result = json.loads(response.data)
  assert isinstance(result, dict)

def test_sobol(client):

  response = client.get(url("sobol"))
  assert response.status_code == 400
  result = json.loads(response.data)
  assert result["code"] == 400

  # invalid dim
  response = client.get(url("sobol", {"dimension": 0, "length": 2}))
  assert response.status_code == 400
  result = json.loads(response.data)
  assert result["code"] == 400

  response = client.get(url("sobol", {"dimension": 2000, "length": 2}))
  assert response.status_code == 400
  result = json.loads(response.data)
  assert result["code"] == 400

  response = client.get(url("sobol", {"dimension": "x", "length": 2}))
  assert response.status_code == 400
  result = json.loads(response.data)
  assert result["code"] == 400

  response = client.get(url("sobol", {"dimension": 2, "length": 2}))
  assert response.status_code == 200
  result = json.loads(response.data)
  assert isinstance(result, list)
  assert len(result) > 0
  assert isinstance(result[0], list)
  assert len(result[0]) > 0


def test_integerise(client):
  input = [1.1, 2.2, 3.3, 4.4]
  response = client.post(url("integerise"), data=json.dumps(input))
  assert response.status_code == 200
  result = json.loads(response.data)
  assert isinstance(result, dict)
  assert "result" in result
  assert "rmse" in result
  assert "conv" in result
  assert result["conv"]

  # invalid (non-integral) mrginal sum
  input = [1.1, 2.2, 3.3, 4.5]
  response = client.post(url("integerise"), data=json.dumps(input))
  assert response.status_code == 400
  result = json.loads(response.data)
  assert isinstance(result, dict)
  assert result["code"] == 400
  assert result["type"] == "RuntimeError"

  input = [[ 0.3,  1.2,  2.0, 1.5],
           [ 0.6,  2.4,  4.0, 3.0],
           [ 1.5,  6.0, 10.0, 7.5],
           [ 0.6,  2.4,  4.0, 3.0]]
  response = client.post(url("integerise"), data=json.dumps(input))
  assert response.status_code == 200
  result = json.loads(response.data)
  assert isinstance(result, dict)
  assert "result" in result
  assert "rmse" in result
  assert "conv" in result
  assert result["conv"]


if __name__ == "__main__":
  unittest.main()
