# Generated by Django 4.0.4 on 2022-04-19 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_album_song_albums_rename_artist_song_artists'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='albums',
            new_name='album',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='artists',
            new_name='artist',
        ),
    ]