# Generated by Django 4.0.4 on 2022-04-24 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_user_exp_sub_playlistfollow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='tags',
        ),
        migrations.AddField(
            model_name='artist',
            name='tags',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.RemoveField(
            model_name='song',
            name='tags',
        ),
        migrations.AddField(
            model_name='song',
            name='tags',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='user',
            name='exp_sub',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 24, 16, 55, 39, 960541)),
        ),
    ]