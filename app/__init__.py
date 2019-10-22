from flask import Flask, jsonify
from flask_graphql import GraphQLView
import os
from .entities.new_schemas import schema
from app.controllers.contacts import bp_contacts
from app.controllers.communities import bp_communities
from app.controllers.assets import bp_assets
from app.settings import flask_config_mapping



def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        flask_config_mapping
    )
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql', schema=schema, graphiql=True)
    )
    prefix = '/api'
    app.register_blueprint(bp_contacts, url_prefix=prefix + '/contacts')  # /api/contacts
    app.register_blueprint(bp_communities, url_prefix=prefix + '/communities')  # /api/contacts
    app.register_blueprint(bp_assets, url_prefix=prefix + '/assets')  # /api/assets


    # leave this for testing whatever
    @app.route('/')
    def hello():
        return 'index :)'
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'message': 'The requested URL was not found on the server.'}), 404

    return app