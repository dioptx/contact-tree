import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_sqlalchemy import SQLAlchemy
from app import db


class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    posts = db.relationship('Post', backref='author')

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))

    def __repr__(self):
        return '<Post %r>' % self.title


class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )
class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       interfaces = (graphene.relay.Node, )


def setup_models(app):
    db = SQLAlchemy()
    return db
