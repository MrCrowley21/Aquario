# Generated by Django 3.2.18 on 2023-06-14 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_alter_sensor_current_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='current_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='current_value',
            field=models.FloatField(blank=True),
        ),
    ]