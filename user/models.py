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
    code = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    nickname = models.CharField(max_length=100)
    fish_id = models.ForeignKey('Fish', on_delete=models.PROTECT)
    volume = models.FloatField()
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    feeding_time = models.DateTimeField()
    # sensors = models.ManyToManyField('Environment')
    water_level = models.FloatField()
    general_system_state = models.FloatField()


class Fish(models.Model):
    fish_type = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    food_id = models.ForeignKey('Food', on_delete=models.PROTECT)


class Food(models.Model):
    food_type = models.CharField(max_length=100)
