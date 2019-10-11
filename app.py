import os
import sys
from flask import Flask
import graphene
from flask_sqlalchemy import SQLAlchemy

from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from entities import schemas, models


db = SQLAlchemy()

# app initialization
def create_app(debug = True):


    app = Flask(__name__)
    app.debug = debug

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Configs
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    schema = schemas.setup_schemas()


    # Routes

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True # for having the GraphiQL interface
        )
    )


    @app.route('/')
    def index():
        return '<p> Hello World</p>'


    return app
if __name__ == '__main__':
     app = create_app()
     app.run()