import maya
from graphql import GraphQLError
from py2neo import Graph, Node
from py2neo.ogm import GraphObject, Property, RelatedTo
import datetime
from app import settings
import flask
import json
from app.contracts.contacts_contract import *
from app.entities.new_models import *
from .common import ok, error, not_found
from app.entities.new_schemas import *

bp_contacts = flask.Blueprint('contacts', __name__)

graph = Graph(
    host=settings.NEO4J_HOST,
    port=settings.NEO4J_PORT,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD,
)


@bp_contacts.route('/', methods=['GET'])
def index():
    return 'bp_contacts index'


@bp_contacts.route('/insert', methods=['POST'])
def create_contact():
    if flask.request.data == '':
        return error('No json data sent.')

    try:
        req = json.loads(flask.request.data)
    except json.decoder.JSONDecodeError as er:
        return error(er)

    try:
        result = ContactContract.from_json(req)
    except TypeError as er:
        return error(er)

    agent = Agent(**result.to_json())
    agent._link_communities()
    agent.save()

    return ok()

@bp_contacts.route('/getbyname', methods=['GET'])
def get_contact():
    if flask.request.data == '':
        return error('No json data sent.')
    try:
        req = json.loads(flask.request.data)
    except json.decoder.JSONDecodeError as er:
        return error(er.with_traceback())
    print(req)

    # Todo: Build Query

    return ok()




