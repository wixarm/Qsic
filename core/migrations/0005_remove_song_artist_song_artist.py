# Generated by Django 4.0.4 on 2022-04-19 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_artist_tags_song_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='artist',
        ),
        migrations.AddField(
            model_name='song',
            name='artist',
            field=models.ManyToManyField(to='core.artist'),
        ),
    ]
