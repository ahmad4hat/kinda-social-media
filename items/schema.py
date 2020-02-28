from .models import Item, Like
import graphene
from graphene_django import DjangoObjectType


class ItemType (DjangoObjectType):
    class Meta:
        model = Item


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class CreateItem(graphene.Mutation):
    item = graphene.Field(ItemType)

    class Arguments:
        type = graphene.String(required=True)
        text = graphene.String(required=True)
        parent_id = graphene.ID()

    def mutate(self, info, type, text, parent_id=None):
        current_user = info.context.user

        if current_user.is_anonymous:
            raise Exception("user not logged in")

        if((type != "post") and (type != "comment")):
            raise Exception("type can not be found")

        if(parent_id == None):
            newItem = Item(type=type, text=text, by=current_user)
            newItem.save()
            return CreateItem(item=newItem)
        parent = Item.objects.get(id=parent_id)
        newItem = Item(type=type, text=text, by=current_user, parent=parent)
        newItem.save()
        return CreateItem(item=newItem)


class Query(graphene.ObjectType):
    items = graphene.List(ItemType)

    def resolve_items(self, info):
        return Item.objects.all()


class Mutation(graphene.ObjectType):
    create_item = CreateItem.Field()
