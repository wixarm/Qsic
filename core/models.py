import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from taggit.managers import TaggableManager


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    exp_sub = models.DateTimeField(default=datetime.datetime.now())
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()


class Reset(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)


# categories
class categories(models.Model):
    name = models.CharField(max_length=50)
    cover = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name


# artist
class artist(models.Model):
    category = models.ForeignKey(categories, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50, verbose_name="Artist Name")
    cover = models.CharField(max_length=300, blank=True)
    tags = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


# album
class album(models.Model):
    artist = models.ManyToManyField(artist)
    name = models.CharField(max_length=300, verbose_name="Album's Name")
    cover = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return str(self.artist) + " - " + str(self.name)


# song
class song(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    artist = models.ManyToManyField(artist)
    album = models.ManyToManyField(album, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    song_link = models.CharField(max_length=500, blank=True)
    video_link = models.CharField(max_length=500, blank=True)
    name = models.CharField(max_length=150)
    cover = models.CharField(max_length=300, blank=True)
    explicit_content = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.name)


# qsic's playlists
class PlayList(models.Model):
    name = models.CharField(max_length=100)
    cover = models.CharField(max_length=300, blank=True)
    Intro = models.TextField(verbose_name="Introduction", blank=True)

    def __str__(self):
        return self.name


class PlayListSong(models.Model):
    song_id = models.ForeignKey(song, max_length=500, on_delete=models.DO_NOTHING)
    playlist = models.ForeignKey(PlayList, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "PlayList: " + str(self.playlist) + " - SongID: " + str(self.song_id)


class PlaylistFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    playlist = models.ForeignKey(PlayList, max_length=500, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Playlist follower"


# favorites
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    song_id = models.ForeignKey(song, max_length=500, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.id


# followers
class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    artist_id = models.ForeignKey(artist, max_length=500, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "follower"



# discount_codes
class discount_code(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    code = models.CharField(max_length=15)
    effect = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    def __str__(self):
        return str(self.code) + " With " + str(self.effect) + " percent of effect"
