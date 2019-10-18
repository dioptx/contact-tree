from flask import Flask, jsonify
from flask_graphql import GraphQLView

from .entities.new_schemas import schema
from app.controllers.contacts import bp_contacts
from app.controllers.assets import bp_assets




def create_app():
    app = Flask(__name__)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql', schema=schema, graphiql=True)
    )
    prefix = '/api'
    app.register_blueprint(bp_contacts, url_prefix=prefix + '/contacts')  # /api/contacts
    app.register_blueprint(bp_assets, url_prefix=prefix + '/assets')  # /api/assets


    # leave this for testing whatever
    @app.route('/')
    def hello():
        return 'index :)'
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'message': 'The requested URL was not found on the server.'}), 404

    return app