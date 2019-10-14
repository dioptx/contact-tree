import graphene

from .models import BaseModel, Contact, Category, Community

class CommunitySchema(graphene.ObjectType):

    name = graphene.String()
    description = graphene.String()

    def __init__(self, **kwargs):
        self._id = kwargs.pop('_id')
        super().__init__(**kwargs)


class CategorySchema(graphene.ObjectType):
    name = graphene.String()
    description = graphene.String()

    def __init__(self, **kwargs):
        self._id = kwargs.pop('_id')
        super().__init__(**kwargs)


class ContactSchema(graphene.ObjectType):
    name = graphene.String()

    communities = graphene.List(CommunitySchema)
    categories = graphene.List(CategorySchema)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contact = Contact(email=self.name).fetch()

    def resolve_categories(self, info):
        return [CategorySchema(**store.as_dict()) for store in self.contact.categories]

    def resolve_communities(self, info):
        return [CommunitySchema(**receipt.as_dict()) for receipt in self.contact.communities]

class CategoryInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)

class CommunityInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)


class CreateContact(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        dateTimeAdded = graphene.String()
        categories = graphene.List(graphene.NonNull(CategoryInput))
        communities = graphene.List(graphene.NonNull(CommunityInput))

    success = graphene.Boolean()
    contact = graphene.Field(lambda: ContactSchema)

    def mutate(self, info, **kwargs):
        contact = Contact(**kwargs)
        contact.save()

        return CreateContact(contact=contact, success=True)

class CreateCommunity(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    success = graphene.Boolean()
    contact = graphene.Field(lambda: ContactSchema)

    def mutate(self, info, **kwargs):
        community = Community(**kwargs)
        community.save()

        return CreateCommunity(contact=community, success=True)


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    success = graphene.Boolean()
    contact = graphene.Field(lambda: ContactSchema)

    def mutate(self, info, **kwargs):
        category = Community(**kwargs)
        category.save()

        return CreateCategory(contact=category, success=True)


class Query(graphene.ObjectType):
    contact = graphene.Field(lambda: ContactSchema, email=graphene.String())
    communities = graphene.List(lambda: CommunitySchema)
    categories = graphene.List(lambda: CategorySchema)

    def resolve_contact(self, info, name):
        contact = Contact(name=name).fetch()
        return ContactSchema(**contact.as_dict())

    def resolve_categories(self, info):
        return [CategorySchema(**category.as_dict()) for category in Category().all]

    def resolve_communities(self, info):
        return [CommunitySchema(**community.as_dict()) for community in Community().all]

class Mutation(graphene.ObjectType):
    create_contact = CreateContact.Field()
    create_community = CreateCommunity.Field()
    create_category = CreateCategory.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)

