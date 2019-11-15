import maya
from graphql import GraphQLError
from py2neo import Graph, Node
from py2neo.ogm import GraphObject, Property, RelatedTo
import datetime
from app import settings
import flask
import json
from app.contracts.contracts import *
from app.entities.new_models import *
from .common import ok, error, not_found, req_to_json
from app.entities.new_schemas import *

bp_agents = flask.Blueprint('agents', __name__)

graph = Graph(
    host=settings.NEO4J_HOST,
    port=settings.NEO4J_PORT,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD,
)


@bp_agents.route('/', methods=['GET'])
def index():
    return 'bp_agents index'


@bp_agents.route('/insert', methods=['POST'])
def create_contact():
    json_req = req_to_json(flask.request.data)

    try:
        result = ContactContract.from_json(json_req)
    except TypeError as er:
        return error("Json request not compatible with the Contract. "
                     "Error: " + str(er))

    agent = Agent(**result.to_json())
    agent.save()
    agent._link_communities()
    agent._link_connections()

    return ok(agent.as_dict())

@bp_agents.route('/getbyname', methods=['GET'])
def get_contact():
    json_req = req_to_json(flask.request.data)

    if "name" not in json_req.keys():
        return error("Contact name value not provided")

    agent = Agent(name= json_req['name']).fetch()
    print(agent.as_dict())
    return ok(agent.as_dict())





