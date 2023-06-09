# Generated by Django 3.2.18 on 2023-05-15 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaterType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water_type', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='aquarium',
            name='feeding_time',
            field=models.TimeField(blank=True, default='8:00'),
        ),
        migrations.AddField(
            model_name='aquarium',
            name='fish_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='user.fish'),
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_value', models.FloatField()),
                ('current_time', models.DateTimeField(blank=True, default=None)),
                ('sensor_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.sensorlist')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendedValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommended_value', models.FloatField()),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.sensor')),
                ('water_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.watertype')),
            ],
        ),
        migrations.AddField(
            model_name='aquarium',
            name='sensors',
            field=models.ManyToManyField(to='user.Sensor'),
        ),
        migrations.AddField(
            model_name='aquarium',
            name='water_type',
            field=models.ManyToManyField(to='user.WaterType'),
        ),
    ]
