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

bp_collections = flask.Blueprint('collections', __name__)


graph = Graph(
    host=settings.NEO4J_HOST,
    port=settings.NEO4J_PORT,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD,
)

@bp_collections.route('/', methods=['GET'])
def index():
    return 'bp_collections index'



@bp_collections.route('/insert', methods=['POST'])
def create_community():
    json_req = req_to_json(flask.request.data)

    try:
        result = CollectionContract.from_json(json_req)
    except TypeError as er:
        return error("Json request not compatible with the Contract. "
                     "Error: " + str(er))

    collection = Collection(**result.to_json())
    collection.save()

    return ok(collection.as_dict())

@bp_collections.route('/getbyname', methods=['GET'])
def get_community():
    json_req = req_to_json(flask.request.data)

    if "name" not in json_req.keys():
        return error("Community name value not provided")

    collection = Collection(name= json_req['name']).fetch()

    return ok(collection.as_dict())

