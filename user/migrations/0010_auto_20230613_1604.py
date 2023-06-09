# Generated by Django 3.2.18 on 2023-06-13 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20230613_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aquarium',
            name='fish_id',
        ),
        migrations.AddField(
            model_name='aquarium',
            name='fish_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user.fish'),
        ),
        migrations.RemoveField(
            model_name='fish',
            name='food_id',
        ),
        migrations.AddField(
            model_name='fish',
            name='food_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user.food'),
        ),
    ]
