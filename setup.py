from setuptools import find_packages, setup
import json

def get_version():
  with open("./app/static/swagger.json") as fp:
    swagger = json.load(fp)
    return swagger["info"]["version"]


setup(
  name='test-appsvc',
  version=get_version(),
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  install_requires=[
    'flask',
    'flask-swagger-ui',
    'python-dotenv',
    'opencensus-ext-azure',
    'humanleague'
  ],
  setup_requires=[
    'pytest-runner'
  ],
  tests_require=[
    'pytest'
  ]
)
