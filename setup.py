from setuptools import find_packages, setup
import json

def get_version():
  with open("./app/static/swagger.json") as fp:
    swagger = json.load(fp)
    return swagger["info"]["version"]


setup(
  name='protoapi',
  version=get_version(),
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  install_requires=[
    'flask',
    'flask-swagger',
    'flask-swagger-ui',
    'humanleague'
  ],
  setup_requires=[
    'pytest-runner'
  ],
  tests_require=[
    'pytest'
  ]
)
