from flask_restplus import Api

from .quionga import API as quionga_api
from .zomic import API as zomic_api

API = Api(
    version="1.0",
    title="Quiongos Webservices",
    description="An API to manage Quiongos Webservices",
)

API.add_namespace(quionga_api, "/quiongos")
API.add_namespace(zomic_api, "/zomic")
