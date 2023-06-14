# Generated by Django 3.2.18 on 2023-06-14 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_sensor_aquarium_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aquarium',
            name='sensors',
        ),
        migrations.AddField(
            model_name='aquarium',
            name='sensors',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='user.sensor'),
        ),
    ]