import logging

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
        )


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = (
            'user',
        )


class AquariumType(DjangoObjectType):
    class Meta:
        model = Aquarium
        fields = (
            'id',
            'code',
            'aquarium_id',
            'nickname',
            'volume',
            'length',
            'width',
            'height',
            'feeding_time',
            'sensors',
            'water_level',
            'general_system_state'
        )


class FishType(DjangoObjectType):
    class Meta:
        model = Fish
        fields = (
            'id',
            'fish_type',
            'common_name',
            'scientific_name',
        )


class AquariumIDs(DjangoObjectType):
    class Meta:
        model = Aquarium
        fields = (
            'id',
            'aquarium_id',
            'code',
        )


class AquariumSensors(DjangoObjectType):
    class Meta:
        model = Aquarium
        fields = (
            'id',
            'sensors',
        )


class Query(ObjectType):
    """
    User queries.
    """
    users = List(UserType)
    user = Field(UserType, id=Int())
    me = Field(UserProfileType)

    aquarium = Field(AquariumType, id=Int())
    fish = Field(FishType)
    aquarium_id = List(AquariumIDs)
    aquarium_sensors = List(AquariumSensors, aquarium_id=Int())

    @staticmethod
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    @staticmethod
    def resolve_user(self, info, **kwargs):
        return User.objects.get(**kwargs)

    @staticmethod
    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Non-authenticated user")
        return UserProfile.objects.get(user=user)

    @staticmethod
    def resolve_aquarium(self, info, **kwargs):
        aquarium = Aquarium.objects.get(**kwargs)
        return aquarium

    @staticmethod
    def resolve_fish(self, info, **kwargs):
        fish = Fish.objects.get(**kwargs)
        return fish

    @staticmethod
    def resolve_aquarium_id(self, info, **kwargs):
        user = info.context.user
        aquarium_data = Aquarium.objects.filter(code=user.id)
        return aquarium_data

    @staticmethod
    def resolve_aquarium_sensors(self, info, aquarium_id, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Non-authenticated user")
        sensors_data = Aquarium.objects.filter(aquarium_id=aquarium_id)
        return sensors_data


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


class RegisterAquarium(Mutation):
    id = ID()
    feedback = String()
    class Arguments:
        aquarium_id = String(required=True)
        nickname = String(required=True)
        # fish_id = String(required=True)
        length = Int()
        width = Int()
        height = Int()
        volume = Int()
        # feeding_time =

    @staticmethod
    def mutate(_, info, aquarium_id, nickname):
        user = info.context.user
        print(info.context)
        if not user.is_authenticated:
            return RegisterAquarium(
                id=None,
                feedback="Non-authenticated user"
            )
        aquarium = Aquarium(
            code=UserProfile.objects.get(user=user.id),
            aquarium_id=aquarium_id,
            nickname=nickname
        )
        aquarium.save()
        return RegisterAquarium(
            id=aquarium.id,
            feedback="Success")


class Mutation(ObjectType):
    """
    Mutations for Users
    """
    create_user = CreateUser.Field()
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    """
    Mutations for aquarium components
    """
    register_aquarium = RegisterAquarium.Field()
