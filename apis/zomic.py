import json
import logging
from datetime import datetime

from flask import Response, g, send_file
from flask_restplus import Namespace, Resource, abort, inputs, reqparse

import settings
from db import zomic as db
from utils import types

LOGGER = logging.getLogger('zomic.ws')

API = Namespace("/zomic", description="Zomic Webservices")

def get_parser_list(member=None, rule=None, proposal=None):
    parser = reqparse.RequestParser()
    parser.add_argument("id",
                        type=int,
                        help="Filter by id")
    parser.add_argument("genesis",
                        type=int,
                        help="Filter by genesis")
    parser.add_argument("active",
                        type=inputs.boolean,
                        help="Filter by status")
    if member:
        parser.add_argument("name",
                            type=str,
                            help="Filter by name")
        parser.add_argument("email",
                            type=types.email,
                            help="Filter by email")
        parser.add_argument("wallet",
                            type=types.wallet,
                            help="Filter by wallet")

    if rule or proposal:
        parser.add_argument("chat_id",
                            type=str,
                            help="Filter by chat_id")
        parser.add_argument("description",
                            type=str,
                            help="Filter by description")

    if proposal:
        parser.add_argument("username",
                            type=str,
                            help="Filter by username (invite)")
    return parser

#################################################################################
############################### WRITE - ENDPOINTS ###############################
#################################################################################
@API.route("/propose")
class Propose(Resource):
    @API.response(501, "Service Not Implemented")
    def post(self):
        """Propose a new rule"""
        abort(code=501, error="ERROR-501-1", status=None,
              message="Service Not Implemented")

@API.route("/invite")
class Invite(Resource):
    @API.response(501, "Service Not Implemented")
    def post(self):
        """Invite a new member"""
        abort(code=501, error="ERROR-501-1", status=None,
              message="Service Not Implemented")

@API.route("/vote")
class Vote(Resource):
    @API.response(501, "Service Not Implemented")
    def post(self):
        """Vote on a proposal"""
        abort(code=501, error="ERROR-501-1", status=None,
              message="Service Not Implemented")

@API.route("/pay_taxes")
class Pay(Resource):
    @API.response(501, "Service Not Implemented")
    def post(self):
        """Pay your taxes"""
        abort(code=501, error="ERROR-501-1", status=None,
              message="Service Not Implemented")

@API.route("/quit")
class Quit(Resource):
    @API.response(501, "Service Not Implemented")
    def post(self):
        """Quit from the community"""
        abort(code=501, error="ERROR-501-1", status=None,
              message="Service Not Implemented")

#################################################################################
############################### READ - ENDPOINTS ################################
#################################################################################
@API.route("/list_members")
class Members(Resource):
    @API.expect(get_parser_list(member=True))
    @API.response(200, "Success")
    def get(self):
        """List community members"""
        args = get_parser_list(member=True).parse_args()
        condition = db.get_where_condition(db.Members,
                                           id=args.id,
                                           genesis=args.genesis,
                                           active=args.active,
                                           name=args.name,
                                           email=args.email,
                                           wallet=args.wallet)

        members = db.Members.select().where(condition)
        return db.get_lines(members, member=True)

@API.route("/list_rules")
class Rules(Resource):
    @API.expect(get_parser_list(rule=True))
    @API.response(200, "Success")
    def get(self):
        """List community rules"""
        args = get_parser_list(rule=True).parse_args()
        condition = db.get_where_condition(db.Rules,
                                           id=args.id,
                                           genesis=args.genesis,
                                           active=args.active,
                                           chat_id=args.chat_id,
                                           description=args.description)

        rules = db.Rules.select().where(condition)
        return db.get_lines(rules, rule=True)

@API.route("/list_proposals")
class Proposals(Resource):
    @API.expect(get_parser_list(proposal=True))
    @API.response(200, "Success")
    def get(self):
        """List community proposals"""
        args = get_parser_list(proposal=True).parse_args()
        condition = db.get_where_condition(db.Proposals,
                                           id=args.id,
                                           genesis=args.genesis,
                                           active=args.active,
                                           chat_id=args.chat_id,
                                           description=args.description,
                                           username=args.username)

        proposals = db.Proposals.select().where(condition)
        return db.get_lines(proposals, proposal=True)

@API.route("/ping")
class Ping(Resource):
    def get(self):
        """Pings the server to ensure it is working as expected"""
        timestamp = datetime.utcnow().strftime(settings.DATETIME)
        LOGGER.warning('/ping ! %s', timestamp)
        return {'status': 'OK'}
