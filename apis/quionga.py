import json
import logging
import psycopg2
from datetime import datetime
from flask import Response, g, send_file
from flask_restplus import Namespace, Resource, abort
try:
    from utils import camera
except ModuleNotFoundError:
    print('Running on Mac: No Camera')

import settings
from db import quionga as db

LOGGER = logging.getLogger('quionga.ws')

API = Namespace("/quionga", description="Quionga Webservices")

def conn():
    if not hasattr(g, 'conn') or g.conn.closed:
        g.conn = psycopg2.connect(settings.DSN)
    return g.conn

@API.route("/ping")
class Ping(Resource):
    def get(self):
        """Pings the server to ensure it is working as expected"""
        timestamp = datetime.utcnow().strftime(settings.DATETIME)
        LOGGER.warning('/ping ! %s', timestamp)
        return {'status': 'OK'}

@API.route("/takepic")
class TakePic(Resource):
    def get(self):
        """Sends a pic taken with the raspberry PI"""
        timestamp = datetime.utcnow().strftime(settings.DATETIME)
        LOGGER.warning('/takepic ! %s', timestamp)
        try:
            camera.take_photo(timestamp+'.jpg')
        except:
            abort(code=503, error="ERROR-503-1", status=None,
                  message="TakePic Service Unavailable At This Moment")

        return send_file(settings.PIC_DIR+timestamp+'.jpg')

@API.route("/receivemail")
class ReceiveMail(Resource):
    def get(self):
        """Receives mail from the server"""
        timestamp = datetime.utcnow().strftime(settings.DATETIME)
        LOGGER.warning('/receivemail ! %s', timestamp)
        abort(code=501, error="ERROR-501-1", status=None,
              message="Send Mail Not Implemented Yet")

@API.route("/checkdb")
class CheckDB(Resource):
    def get(self):
        """Check DB status"""
        timestamp = datetime.utcnow().strftime(settings.DATETIME)
        LOGGER.warning('/checkdb ! %s', timestamp)

        exists = True if db.exists(conn(), 'test', "name = %(name)s", {"name": "test"}) else False
        count = db.count(conn(), 'test', "name = %(name)s", {"name": "test"})

        sql = "select * from test where name = %(name)s"
        select = db.execute(conn(), sql, {"name": "test"}, fetch="all")

        return Response(json.dumps(dict(exists=exists,
                                        count=count,
                                        select=select), indent=2), mimetype='application/json')
