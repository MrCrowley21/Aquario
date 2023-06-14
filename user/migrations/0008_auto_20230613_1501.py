# Generated by Django 3.2.18 on 2023-06-13 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_aquarium_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fish',
            name='food_id',
        ),
        migrations.AddField(
            model_name='fish',
            name='food_id',
            field=models.ManyToManyField(to='user.Food'),
        ),
    ]