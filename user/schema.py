import logging
from datetime import datetime, timedelta

import graphene
import graphql_jwt
from graphene import Mutation, ObjectType, List, Field, Int, String, ID, Time, DateTime, Float
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from user.models import *
from user.ideal_value_resolver import *


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
            'fish_id',
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
            "food_id",
        )


class FeedingTime(DjangoObjectType):
    class Meta:
        model = Aquarium
        fields = (
            'feeding_time',
        )


class FoodType(DjangoObjectType):
    class Meta:
        model = Food
        fields = (
            'id',
            'food_type',
        )


class AquariumIDs(DjangoObjectType):
    class Meta:
        model = Aquarium
        fields = (
            'id',
            'aquarium_id',
            'code',
            'nickname',
        )


class FishTypeWater(DjangoObjectType):
    class Meta:
        model = WaterType
        fields = (
            'id',
            'water_type',
        )


class AquariumSensors(DjangoObjectType):
    class Meta:
        model = Aquarium
        fields = (
            'id',
            'sensors',
        )


class SensorType(DjangoObjectType):
    class Meta:
        model = Sensor
        fields = (
            'id',
            'sensor_name',
            'sensor_type',
            'current_value',
            'current_time',
            'ideal_value',
        )


class SingleSensorType(DjangoObjectType):
    class Meta:
        model = Sensor
        fields = (
            'id',
            'sensor_name',
            'sensor_type',
            'current_value',
            'current_time',
            'ideal_value',
        )


class SensorListType(DjangoObjectType):
    class Meta:
        model = SensorList
        fields = (
            'id',
            'sensor_name',
            'sensor_type',
        )


class SensorHistoryType(DjangoObjectType):
    class Meta:
        model = SensorHistory.history.model
        fields = (
            'id',
            'sensor_id',
            'aquarium_id',
            'sensor_value',
            'sensor_time',
            'time_period',
            'nr_records',
        )


class Query(ObjectType):
    """
    User queries.
    """
    users = List(UserType)
    user = Field(UserType, id=Int())
    me = Field(UserProfileType)

    aquarium = Field(AquariumType, id=Int())
    fish = List(FishType)
    fish_type = List(FishTypeWater)
    food = List(FoodType)
    aquarium_id = List(AquariumIDs)
    aquarium_sensors = List(AquariumSensors, aquarium_id=String())
    feeding_time = List(FeedingTime, aquarium_id=String())
    sensor_type = List(SensorType, aquarium_id=String())
    single_sensor_type = Field(SingleSensorType, aquarium_id=String(), sensor_id=Int())
    sensor_list_type = List(SensorListType)
    sensor_history = List(SensorHistoryType, sensor_id=Int(), aquarium_id=String(), time_period=String(),
                          nr_records=Int())
    mean_value = Float(sensor_id=Int(), aquarium_id=String(), time_period=String())
    max_value = Float(sensor_id=Int(), aquarium_id=String(), time_period=String())
    min_value = Float(sensor_id=Int(), aquarium_id=String(), time_period=String())

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
        sensors_data = []
        aquarium = Aquarium.objects.get(**kwargs)
        sensors = aquarium.sensors.all()
        for sensor in sensors:
            sensor_value = check_parameter(sensor.sensor_type, sensor.current_value)
            sensors_data.append(sensor_value)
        system_state = get_system_state(sensors_data)
        aquarium.general_system_state = system_state
        return aquarium

    @staticmethod
    def resolve_fish(self, info, **kwargs):
        fish = Fish.objects.all()
        return fish

    @staticmethod
    def resolve_fish_type(self, info, **kwargs):
        fish_type = WaterType.objects.all()
        return fish_type

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

    @staticmethod
    def resolve_food(self, info, **kwargs):
        food = Food.objects.all()
        return food

    @staticmethod
    def resolve_feeding_time(self, info, aquarium_id, **kwargs):
        print(aquarium_id)
        return Aquarium.objects.filter(aquarium_id=aquarium_id)

    @staticmethod
    def resolve_sensor_type(self, info, aquarium_id, **kwargs):
        aquarium_obj = Aquarium.objects.get(aquarium_id=aquarium_id)
        return Sensor.objects.filter(aquarium_id=aquarium_obj)

    @staticmethod
    def resolve_single_sensor_type(self, info, aquarium_id, sensor_id, **kwargs):
        aquarium_obj = Aquarium.objects.get(aquarium_id=aquarium_id)
        return Sensor.objects.get(aquarium_id=aquarium_obj, id=sensor_id)

    @staticmethod
    def resolve_sensor_list_type(self, info, aquarium_id, **kwargs):
        return SensorList.objects.all()

    @staticmethod
    def resolve_sensor_history(self, info, sensor_id, aquarium_id, time_period, nr_records, **kwargs):
        # aquarium_obj = Aquarium.objects.get(aquarium_id=aquarium_id)
        # sensor_obj = Sensor.objects.get(sensor_id=sensor_id, aquarium_id=aquarium_obj)
        period = time_period.upper()
        if period == "YEAR":
            nr_days = 365
        elif period == "MONTH":
            nr_days = 30
        elif period == "WEEK":
            nr_days = 7
        else:
            nr_days = 1
        time_past = datetime.now() - timedelta(days=nr_days)
        sensor_history = SensorHistory.objects.get(sensor_id=sensor_id, aquarium_id=aquarium_id)
        history_records = sensor_history.history.filter(sensor_time__gt=time_past)
        total_records = history_records.count()
        step_size = max(total_records // (nr_records - 1), 1)
        output_records = history_records[::step_size]
        return output_records

    @staticmethod
    def resolve_mean_value(self, info, aquarium_id, sensor_id, time_period):
        period = time_period.upper()
        if period == "YEAR":
            nr_days = 365
        elif period == "MONTH":
            nr_days = 30
        elif period == "WEEK":
            nr_days = 7
        else:
            nr_days = 1
        time_past = datetime.now() - timedelta(days=nr_days)
        sensor_history = SensorHistory.objects.get(sensor_id=sensor_id, aquarium_id=aquarium_id)
        history_records = sensor_history.history.filter(sensor_time__gt=time_past)
        values = [history.sensor_value for history in history_records]
        if len(values) > 0:
            mean = sum(values) / len(values)
        else:
            mean = 0
        return mean

    @staticmethod
    def resolve_max_value(self, info, aquarium_id, sensor_id, time_period):
        period = time_period.upper()
        if period == "YEAR":
            nr_days = 365
        elif period == "MONTH":
            nr_days = 30
        elif period == "WEEK":
            nr_days = 7
        else:
            nr_days = 1
        time_past = datetime.now() - timedelta(days=nr_days)
        sensor_history = SensorHistory.objects.get(sensor_id=sensor_id, aquarium_id=aquarium_id)
        history_records = sensor_history.history.filter(sensor_time__gt=time_past)
        values = [history.sensor_value for history in history_records]
        max_rec = max(values)
        return max_rec

    @staticmethod
    def resolve_min_value(self, info, aquarium_id, sensor_id, time_period):
        period = time_period.upper()
        if period == "YEAR":
            nr_days = 365
        elif period == "MONTH":
            nr_days = 30
        elif period == "WEEK":
            nr_days = 7
        else:
            nr_days = 1
        time_past = datetime.now() - timedelta(days=nr_days)
        sensor_history = SensorHistory.objects.get(sensor_id=sensor_id, aquarium_id=aquarium_id)
        history_records = sensor_history.history.filter(sensor_time__gt=time_past)
        values = [history.sensor_value for history in history_records]
        min_rec = min(values)
        return min_rec


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
        fish_id = Int()
        length = Int()
        width = Int()
        height = Int()
        volume = Int()
        feeding_time = Time()

    @staticmethod
    def mutate(_, info, aquarium_id, nickname, fish_id, feeding_time, length, width, height, volume):
        user = info.context.user
        # print(info.context)
        if not user.is_authenticated:
            return RegisterAquarium(
                id=None,
                feedback="Non-authenticated user"
            )
        aquarium = Aquarium(
            code=UserProfile.objects.get(user=user.id),
            aquarium_id=aquarium_id,
            nickname=nickname,
        )
        if feeding_time is not None:
            aquarium.feeding_time = feeding_time
        if length is not None:
            aquarium.length = length
        if width is not None:
            aquarium.width = width
        if height is not None:
            aquarium.height = height
        if volume is not None:
            aquarium.volume = volume
        aquarium.save()
        try:
            # print(Fish.objects.all())
            fish_obj = Fish.objects.get(id=fish_id)
            aquarium.fish_id.add(fish_obj)
        except:
            logging.info("Non-valid fish")
            print("Fish fail")
        return RegisterAquarium(
            id=aquarium.id,
            feedback="Success")


class ModifyAquariumData(Mutation):
    id = ID()
    feedback = String()

    class Arguments:
        aquarium_id = String(required=True)
        nickname = String(required=False)
        fish_id = Int(required=False)
        feeding_time = graphene.Time(required=False)

    @staticmethod
    def mutate(_, info, aquarium_id, nickname, feeding_time, fish_id):
        user = info.context.user
        # print(info.context)
        if not user.is_authenticated:
            return RegisterAquarium(
                id=None,
                feedback="Non-authenticated user"
            )

        aquarium = Aquarium.objects.get(code=UserProfile.objects.get(user=user.id), aquarium_id=aquarium_id)

        if nickname is not None:
            aquarium.nickname = nickname
        if feeding_time is not None:
            aquarium.feeding_time = feeding_time
        aquarium.save()
        try:
            fish_obj = Fish.objects.get(id=fish_id)
            aquarium.fish_id.add(fish_obj)
        except:
            logging.info("Non-valid fish")

        return ModifyAquariumData(
            id=aquarium.id,
            feedback="Success")


class AddSensor(Mutation):
    id = ID()
    feedback = String()

    class Arguments:
        aquarium_id = String(required=True)
        sensor_name = String(required=True)
        sensor_type = String(required=True)
        ideal_value = Float()

    @staticmethod
    def mutate(_, info, aquarium_id, sensor_name, sensor_type):
        print(SensorList.objects.get(sensor_name=sensor_name))
        aquarium_obj = Aquarium.objects.get(aquarium_id=aquarium_id)
        sensor = Sensor(
            aquarium_id=aquarium_obj,
            sensor_name=SensorList.objects.get(sensor_name=sensor_name),
            sensor_type=sensor_type.upper(),
            ideal_value=get_ideal_sensor_value(sensor_type.upper())
        )
        sensor.save()
        sensor_history = SensorHistory(
            aquarium_id=aquarium_id,
            sensor_id=sensor.id)
        # sensor_history.sensor_id.add(sensor)
        sensor_history.save()
        aquarium_obj.sensors.add(sensor)
        return AddSensor(
            id=sensor.id,
            feedback="Success")


class UpdateSensor(Mutation):
    id = ID()
    feedback = String()

    class Arguments:
        pk = Int(required=True)
        aquarium_id = String(required=True)
        current_value = Float(required=True)
        current_time = DateTime(required=True)
    # 2023-06-14T14:49:00+02:00
    @staticmethod
    def mutate(_, info, pk, aquarium_id, current_value, current_time):
        aquarium_obj = Aquarium.objects.get(aquarium_id=aquarium_id)
        sensor = Sensor.objects.get(aquarium_id=aquarium_obj, pk=pk)
        sensor.current_value = current_value
        sensor.current_time = current_time
        sensor.save()
        sensor_history = SensorHistory.objects.get(aquarium_id=aquarium_id, sensor_id=sensor.id)
        # sensor_history = SensorHistory.objects.create(aquarium_id=aquarium_obj)
        # sensor_history.sensor_id.add(sensor)
        sensor_history.sensor_value = current_value
        sensor_history.sensor_time = current_time
        sensor_history.save()
        return UpdateSensor(
            id=sensor.id,
            feedback="Success")


class UpdateWaterLevel(Mutation):
    id = ID()
    feedback = String()

    class Arguments:
        aquarium_id = String(required=True)
        water_level = Float(required=True)

    @staticmethod
    def mutate(_, info, aquarium_id, water_level):
        aquarium = Aquarium.objects.get(aquarium_id=aquarium_id)
        aquarium.water_level = water_level
        aquarium.save()
        return UpdateSensor(
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
    modify_aquarium = ModifyAquariumData.Field()
    add_sensor = AddSensor.Field()
    update_sensor = UpdateSensor.Field()
    update_water_level = UpdateWaterLevel.Field()
