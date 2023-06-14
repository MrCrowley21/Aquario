from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import math


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserProfile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Aquarium(models.Model):
    code = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    aquarium_id = models.CharField(max_length=20, default=None)
    nickname = models.CharField(max_length=100)
    fish_id = models.ManyToManyField('Fish')
    volume = models.FloatField(default=0)
    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    feeding_time = models.TimeField(default='8:00', blank=True)
    water_type = models.ForeignKey('WaterType', default=1, on_delete=models.CASCADE)
    water_level = models.FloatField(default=86.0)
    sensors = models.ManyToManyField('Sensor', default=None)
    general_system_state = models.FloatField(default=0)


class Fish(models.Model):
    fish_type = models.ForeignKey('WaterType', on_delete=models.PROTECT)
    common_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    food_id = models.ForeignKey('Food', on_delete=models.PROTECT)


class Food(models.Model):
    food_type = models.CharField(max_length=100)


class WaterType(models.Model):
    water_type = models.CharField(max_length=20, blank=False,  unique=True)


class RecommendedValues(models.Model):
    water_type = models.ForeignKey('WaterType', on_delete=models.PROTECT)
    sensor = models.ForeignKey('Sensor', on_delete=models.PROTECT)
    fish_type = models.ForeignKey('Fish', on_delete=models.PROTECT, default=None)
    recommended_value = models.FloatField()


class SensorList(models.Model):
    sensor_name = models.CharField(max_length=20, unique=True)


class Sensor(models.Model):
    aquarium_id = models.ForeignKey('Aquarium', default=None, on_delete=models.PROTECT)
    SENSOR_CHOICE = [
        ("TEMPERATURE", "Temperature"),
        ("PH", "PH"),
        ("OXYGEN", "Oxygen"),
        ("TURBIDITY", "Turbidity"),
        ("NITRATE", "Nitrate"),
        ("DURITY", "Durity"),
        ("AMMONIUM", "Ammonium"),
    ]
    sensor_type = models.CharField(
        max_length=11,
        choices=SENSOR_CHOICE,
        default="TEMPERATURE",
    )
    sensor_name = models.ForeignKey('SensorList', on_delete=models.PROTECT)
    current_value = models.FloatField(blank=True, default=0.0)
    current_time = models.DateTimeField(blank=True, default="1900-01-01 00:00")
    ideal_value = models.FloatField(default=0)

