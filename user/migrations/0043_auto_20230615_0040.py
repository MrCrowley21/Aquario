# Generated by Django 3.2.18 on 2023-06-14 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0042_auto_20230615_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsensorhistory',
            name='aquarium_id',
        ),
        migrations.RemoveField(
            model_name='historicalsensorhistory',
            name='sensor_id',
        ),
    ]
