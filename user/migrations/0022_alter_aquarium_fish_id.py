# Generated by Django 3.2.18 on 2023-06-13 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_alter_aquarium_fish_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aquarium',
            name='fish_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.fish'),
        ),
    ]
