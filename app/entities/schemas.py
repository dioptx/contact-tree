import graphene

from .models import *


class Query(graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)

