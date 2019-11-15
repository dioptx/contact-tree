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

bp_communities = flask.Blueprint('communities', __name__)


graph = Graph(
    host=settings.NEO4J_HOST,
    port=settings.NEO4J_PORT,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD,
)

@bp_communities.route('/', methods=['GET'])
def index():
    return 'bp_communities index'



@bp_communities.route('/insert', methods=['POST'])
def create_community():
    json_req = req_to_json(flask.request.data)

    try:
        result = CommunityContract.from_json(json_req)
    except TypeError as er:
        return error("Json request not compatible with the Contract. "
                     "Error: " + str(er))

    community = Community(**result.to_json())
    community.save()

    return ok(community.as_dict())

@bp_communities.route('/getbyname', methods=['GET'])
def get_community():
    json_req = req_to_json(flask.request.data)

    if "name" not in json_req.keys():
        return error("Community name value not provided")

    community = Community(name= json_req['name']).fetch()

    return ok(community.as_dict())

