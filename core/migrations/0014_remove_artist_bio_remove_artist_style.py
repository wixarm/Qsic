# Generated by Django 4.0.4 on 2022-04-20 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_artist_style'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='style',
        ),
    ]