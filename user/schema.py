import graphql_jwt
from graphene import Mutation, ObjectType, List, Field, Int, String, ID
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from user.models import *


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
        )


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = (
            'user',
        )


class Query(ObjectType):
    """
    User queries.
    """
    users = List(UserType)
    user = Field(UserType, id=Int())

    @staticmethod
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    @staticmethod
    def resolve_user(self, info, **kwargs):
        return User.objects.get(**kwargs)


class CreateUser(Mutation):
    id = ID()

    class Arguments:
        email = String(required=True)
        password = String(required=True)

    @staticmethod
    def mutate(_, info, email, password):
        user = User.objects.create_user(email=email,
                                        password=password,
                                        )
        return CreateUser(id=user.id)


class Mutation(ObjectType):
    """
    Mutations for Users.
    """
    create_user = CreateUser.Field()
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    """
    User Profiles
    """

    # update_user_profile = UpdateUserProfile.Field()
