# Generated by Django 3.2.18 on 2023-06-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0028_alter_aquarium_sensors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aquarium',
            name='sensors',
        ),
        migrations.AddField(
            model_name='aquarium',
            name='sensors',
            field=models.ManyToManyField(to='user.Sensor'),
        ),
    ]
