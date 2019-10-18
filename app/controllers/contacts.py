import maya
from graphql import GraphQLError
from py2neo import Graph, Node
from py2neo.ogm import GraphObject, Property, RelatedTo
import datetime
from app import settings
import flask
import json
from app.contracts.contacts import *
from app.entities.new_models import *
from .common import ok, error, not_found

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
    req = ContactContract.from_json(json.loads(flask.request.data))

    #validate
    pass

    # new_contact = Agent()
    # new_contact.save

    print(req)
    return ok()