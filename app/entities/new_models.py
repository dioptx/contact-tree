import maya
from graphql import GraphQLError
from py2neo import Graph, Node
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




class Community(BaseModel):
    __primarykey__ = 'name'

    name = Property()
    description = Property()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fetch(self):
        community = self.match(graph, self.name).first()
        if community is None:
            raise GraphQLError(F"{self.name} has not been found in our community list.")

        return community

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'description': self.description
        }

class Agent(BaseModel):

    __primarykey__ = 'name'

    name = Property()
    dateTimeAdded = Property(default= datetime.datetime.utcnow())

    knows = RelatedTo('Agent', 'KNOWS')
    belongs = RelatedTo('Community', 'BELONGS')
    tags = Property()

    email = Property()
    loves = Property()
    hates = Property()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dateTimeAdded = datetime.datetime.utcnow()


    def link_connections(self, connections):
        for name in connections:
            agent = Agent(name= name).fetch()
            agent.knows.add(self)
            agent.save()
        return

    def link_communities(self, communities):
        for name in communities:
            community = Community(name= name).fetch()
            agent = Agent(name=self.name).fetch()
            agent.belongs.add(community)
            agent.save()

        return


    def fetch(self):
        agent = self.match(graph, self.name).first()
        if agent is None:
            raise GraphQLError(F"{self.name} has not been found in our agent list.")

        return agent

    def fetch_knows(self):

        return [{
            **agent[0].as_dict(),
            **agent[1]
        } for agent in self.knows._related_objects]

    def fetch_belongs(self):
        return [{
            **com[0].as_dict(),
            **com[1]
        } for com in self.belongs._related_objects]

    def as_dict(self):
        return {
            'name': self.name,
            'knows': [agent for agent in self.knows],
            'belongs': [community for community in self.belongs],
            'email': self.email
        }

