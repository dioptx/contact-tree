import graphene
import datetime
from .models import Customer, Store, Receipt, Product, Agent, Community


class ProductSchema(graphene.ObjectType):
    name = graphene.String()
    brand = graphene.String()
    category = graphene.String()

    price = graphene.Float()
    amount = graphene.Int()


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    amount = graphene.Int(required=True)


class StoreSchema(graphene.ObjectType):
    name = graphene.String()
    address = graphene.String()

    products = graphene.List(ProductSchema)

    def __init__(self, **kwargs):
        self._id = kwargs.pop('_id')
        super().__init__(**kwargs)

    def resolve_products(self, info):
        return [ProductSchema(**product) for product in Store().fetch(self._id).fetch_products()]


class StoreInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    address = graphene.String(required=True)


class ReceiptSchema(graphene.ObjectType):
    total_amount = graphene.Float()
    timestamp = graphene.String()

    products = graphene.List(ProductSchema)

    def __init__(self, **kwargs):
        self._id = kwargs.pop('_id')
        super().__init__(**kwargs)

    def resolve_products(self, info):
        return [ProductSchema(**product) for product in Receipt().fetch(self._id).fetch_products()]


class SubmitReceipt(graphene.Mutation):
    class Arguments:
        customer_email = graphene.String(required=True)
        products = graphene.List(graphene.NonNull(ProductInput))
        store = StoreInput(required=True)
        timestamp = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, **kwargs):
        customer = Customer(email=kwargs.pop('customer_email')).fetch()
        customer.submit_receipt(**kwargs)

        return SubmitReceipt(success=True)


class CustomerSchema(graphene.ObjectType):
    email = graphene.String()
    name = graphene.String()

    stores = graphene.List(StoreSchema)
    receipts = graphene.List(ReceiptSchema)
    products = graphene.List(ProductSchema)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.customer = Customer(email=self.email).fetch()

    def resolve_stores(self, info):
        return [StoreSchema(**store.as_dict()) for store in self.customer.stores]

    def resolve_receipts(self, info):
        return [ReceiptSchema(**receipt.as_dict()) for receipt in self.customer.receipts]

    def resolve_products(self, info):
        return [ProductSchema(**product.as_dict()) for product in self.customer.products]



class AgentSchema(graphene.ObjectType):
    name = graphene.String()
    knownFrom = graphene.List(graphene.String)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.agent = Agent(name= self.name).fetch()

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    success = graphene.Boolean()
    customer = graphene.Field(lambda: CustomerSchema)

    def mutate(self, info, **kwargs):
        customer = Customer(**kwargs)
        customer.save()

        return CreateCustomer(customer=customer, success=True)

class CreateAgent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        dateTimeAdded = graphene.DateTime()
        knows = graphene.List(graphene.String)
        belongs = graphene.List(graphene.String)


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
    customer = graphene.Field(lambda: CustomerSchema, email=graphene.String())
    stores = graphene.List(lambda: StoreSchema)
    products = graphene.List(lambda: ProductSchema)
    agent = graphene.Field(lambda: AgentSchema, name=graphene.String())
    community = graphene.Field(lambda: CommunitySchema, name=graphene.String())

    def resolve_customer(self, info, email):
        customer = Customer(email=email).fetch()
        return CustomerSchema(**customer.as_dict())

    def resolve_stores(self, info):
        return [StoreSchema(**store.as_dict()) for store in Store().all]

    def resolve_products(self, info):
        return [ProductSchema(**product.as_dict()) for product in Product().all]


class Mutations(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    submit_receipt = SubmitReceipt.Field()
    create_community = CreateCommunity.Field()
    create_agent = CreateAgent.Field()


schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)
