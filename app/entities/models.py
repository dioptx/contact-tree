from builtins import property, hasattr, setattr

import maya
from graphql import GraphQLError
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo
import datetime
from app import settings



graph = Graph(
    host=settings.NEO4J_HOST,
    port=settings.NEO4J_PORT,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD,
)


class BaseModel(GraphObject):
    """
    Implements some basic functions to guarantee some standard functionality
    across all models. The main purpose here is also to compensate for some
    missing basic features that we expected from GraphObjects, and improve the
    way we interact with them.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def all(self):
        return self.match(graph)

    def save(self):
        graph.push(self)

class Contact(BaseModel):
    __primarykey__ = 'name'
    categories = RelatedTo('Category', 'BELONGS')
    communities = RelatedTo('Community', 'BELONGS')
    name = Property()
    dateTimeAdded = Property(default= datetime.datetime.utcnow)

    def fetch(self):
        contact = self.match(graph, self.name).first()
        if contact is None:
            raise GraphQLError(F"{self.name} has not been found in our customers list.")

        return contact

    def as_dict(self):
        return {
            'name': self.name,
            'timestamp': maya.parse(self.dateTimeAdded),
            'categories': self.fetch_categories()
        }

    def fetch_categories(self):
        """
        Fetches the categories of a contact
        :return:
        """
        return [{
            **category[0].as_dict(),
            **category[1]
        } for category in self.categories._related_objects]

class Community(BaseModel):
    __primarykey__ = 'name'

    name = Property()
    description = Property()

    def fetch(self, _id):
        return Community.match(graph, _id).first()

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'description': self.description
        }

class Category(BaseModel):

    name = Property()
    description = Property()

    def fetch(self, _id):
        return Category.match(graph, _id).first()

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'description': self.description
        }


# # SQL
# class Contact(db.Model):
#     __tablename__ = 'contacts'
#     uuid = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(256), index=True, unique=True)
#     category = db.relationship('Category', backref='author')
#     timestampAdded = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
#     links =
#     def __repr__(self):
#         return '<User %r>' % self.username
#
# class Category(db.Model):
#     __tablename__ = 'categories'
#     uuid = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(256), index=True, unique=True)
#     description = db.Column(db.String(512), index=True)
#
#
#
# # GraphQL
# class ContactObject(SQLAlchemyObjectType):
#    class Meta:
#        model = Contact
#        interfaces = (graphene.relay.Node,)
#
# class CategoryObject(SQLAlchemyObjectType):
#     class Meta:
#         model = Category
#         interfaces = (graphene.relay.Node,)

# class Post(db.Model):
#     __tablename__ = 'posts'
#     uuid = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(256), index=True)
#     body = db.Column(db.Text)
#     author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
#
#     def __repr__(self):
#         return '<Post %r>' % self.title
#
#
# class PostObject(SQLAlchemyObjectType):
#     class Meta:
#         model = Post
#         interfaces = (graphene.relay.Node,)
#


