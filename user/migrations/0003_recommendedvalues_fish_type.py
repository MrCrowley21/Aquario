# Generated by Django 3.2.18 on 2023-05-15 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20230515_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendedvalues',
            name='fish_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='user.fish'),
        ),
    ]
