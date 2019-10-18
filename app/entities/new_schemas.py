import graphene
import datetime
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

        self.agent = Agent(name= self.name).fetch()



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
        # contact.__verify_communities(communities= kwargs.pop('communities'))
        agent.dateTimeAdded = datetime.datetime.utcnow()
        agent.save()
        if kwargs.get('knows') != None:
            agent.link_connections(connections=kwargs.get('knows'))

        if kwargs.get('belongs') != None:
            agent.link_communities(communities=kwargs.get('belongs'))



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





class Query(graphene.ObjectType):
    agent = graphene.Field(lambda: AgentSchema, name=graphene.String())
    community = graphene.Field(lambda: CommunitySchema, name= graphene.String())


class Mutations(graphene.ObjectType):
    create_agent = CreateAgent.Field()
    create_community = CreateCommunity.Field()

schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)
