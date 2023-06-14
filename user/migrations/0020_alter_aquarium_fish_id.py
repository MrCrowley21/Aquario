# Generated by Django 3.2.18 on 2023-06-13 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_alter_aquarium_fish_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aquarium',
            name='fish_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='user.fish'),
        ),
    ]