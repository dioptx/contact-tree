import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from entities import models
from flask_sqlalchemy import SQLAlchemy
from app import db
from entities.models import *

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(models.PostObject)
    all_users = SQLAlchemyConnectionField(models.UserObject)

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        username = graphene.String(required=True)
    post = graphene.Field(lambda: PostObject)
    def mutate(self, info, title, body, username):
        user = User.query.filter_by(username=username).first()
        post = Post(title=title, body=body)
        if user is not None:
            post.author = user
        db.session.add(post)
        db.session.commit()
        return CreatePost(post=post)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()



def setup_schemas():
    schema = graphene.Schema(query=Query, mutation=Mutation)
    return schema

