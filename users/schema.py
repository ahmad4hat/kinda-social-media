from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import Friend
import graphene


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class FriendType(DjangoObjectType):
    class Meta:
        model = Friend


class AddFriend(graphene.Mutation):
    user = graphene.Field(UserType)
    friend = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("user not logged in")
        friend = get_user_model().objects.get(id=id)

        friend1 = Friend.objects.create(
            user=friend,
            friend=current_user
        )
        friend2 = Friend.objects.create(
            user=current_user,
            friend=friend
        )
        friend1.save()
        friend2.save()

        return AddFriend(user=current_user, friend=friend)


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType)

    def resolve_user(self, info, id):
        print(get_user_model().objects.get(id=id))
        return get_user_model().objects.get(id=id)

    def resolve_me(self, info):
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("user not logged in")
        return current_user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    add_friend = AddFriend.Field()
