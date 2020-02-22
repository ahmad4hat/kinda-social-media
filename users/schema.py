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

        print(current_user.username)
        print(friend.username)
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


class RemoveFriend(graphene.Mutation):
    friend_id = graphene.Int()

    class Arguments:
        friend_id = graphene.Int(required=True)

    def mutate(self, info, friend_id):
        current_user = info.context.user
        if current_user.is_anonymous:
            raise Exception("user not logged in")

        print("here 1 after authentication")

        friend = get_user_model().objects.get(id=friend_id)
        userFriendList = Friend.objects.get(
            friend_id=friend_id, user_id=current_user.id)

        friendFriendList = Friend.objects.get(
            friend_id=current_user.id, user_id=friend_id)

        a = current_user.friends.filter(id=friendFriendList.id)
        b = friend.friends.filter(id=userFriendList.id)
        a.delete()
        b.delete()

        # print(a)
        # print(b)

        current_user.save()
        # friend.friends.remove()

        # current_user.save()
        # friend.save()

        # userFriendList.remove()
        # friendFriendList.remove()
        print(current_user.friends.all())

        # print(userFriendList.user_id)
        # print(friendFriendList.user_id)

        # friend_1 = Friend.objects.get(user=current_user, friend=friend)
        # friend_2 = Friend.objects.get(user=friend, friend=current_user)
        # friend_1.remove()
        # friend_2.remove()
        # print(friend_2.user.friends)

        return RemoveFriend(friend_id)


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
    remove_friend = RemoveFriend.Field()
