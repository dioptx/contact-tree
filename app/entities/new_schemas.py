from collections import namedtuple

import graphene
import datetime

import json
from .new_models import Agent, Community

class AgentSchema(graphene.ObjectType):
    name = graphene.String(required=True)
    dateTimeAdded = graphene.DateTime()
    knows = graphene.List(graphene.String)
    belongs = graphene.List(graphene.String)
    tags = graphene.List(graphene.String)
    email = graphene.String(required=False)
    loves = graphene.String(required=False)
    hates = graphene.String(required=False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.pop('name')
        self.agent = Agent(name= self.name)

    def resolve_knows(self, info):
        _agent = Agent(name= self.name).fetch()

        # Todo: find out how to return who knows

        return _agent.knows

    def resolve_belongs(self, info):
        # Todo: build funcitonality
        _agent = Agent(name=self.name).fetch()

        return _agent.belongs


class CreateAgent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        dateTimeAdded = graphene.DateTime()
        knows = graphene.List(graphene.String)
        belongs = graphene.List(graphene.String)
        tags = graphene.List(graphene.String)
        email = graphene.String(required=False)
        loves = graphene.String(required=False)
        hates = graphene.String(required=False)

    success = graphene.Boolean()
    agent = graphene.Field(lambda: AgentSchema)

    def mutate(self, info, **kwargs):

        agent = Agent(**kwargs)
        agent.save()
        if kwargs.get('knows') != None:
            # agent.link_connections(connections=kwargs.get('knows'))
            agent._link_connections(connections=kwargs.get('knows'))
        if kwargs.get('belongs') != None:
            agent._link_communities(communities=kwargs.get('belongs'))


        return CreateAgent(agent=agent, success=True)


class CommunitySchema(graphene.ObjectType):

    name = graphene.String()
    description = graphene.String()

    def __init__(self, **kwargs):
        self._id = kwargs.pop('_id')
        super().__init__(**kwargs)



class CreateCommunity(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    success = graphene.Boolean()
    community = graphene.Field(lambda: CommunitySchema)

    def mutate(self, info, **kwargs):
        community = Community(**kwargs)
        community.save()

        return CreateCommunity(community=community, success=True)


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


class Query(graphene.ObjectType):
    agent = graphene.Field(lambda: AgentSchema, name=graphene.String(required=True))
    community = graphene.Field(lambda: CommunitySchema, name= graphene.String())

    def resolve_agent(self, info, name):
        agent = Agent(name=name)

        return AgentSchema(**agent.as_dict())


class Mutations(graphene.ObjectType):
    create_agent = CreateAgent.Field()
    create_community = CreateCommunity.Field()

schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)
