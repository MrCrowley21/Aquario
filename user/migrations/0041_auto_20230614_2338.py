# Generated by Django 3.2.18 on 2023-06-14 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0040_auto_20230614_2332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensorhistory',
            name='sensor_id',
        ),
        migrations.AddField(
            model_name='sensorhistory',
            name='sensor_id',
            field=models.ManyToManyField(to='user.Sensor'),
        ),
    ]