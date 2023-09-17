from django.contrib import admin
from . import models
from admin_searchable_dropdown.filters import AutocompleteFilter
from .models import User


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'exp_sub', 'is_superuser')
    search_fields = ('email',)
    fieldsets = (
        (None, {
            'fields': ('email', 'password', 'exp_sub', 'is_superuser', 'is_staff',), }),)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'exp_sub'), }),)
    ordering = ('email',)
    list_per_page = 50


admin.site.register(User, MyUserAdmin)


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ['category', ]
    list_per_page = 50

    class Meta:
        model = models.song


admin.site.register(models.artist, ArtistAdmin)


class AlbumAdmin(admin.ModelAdmin):
    raw_id_fields = ('artist',)
    list_display = ('name', 'song_artists')
    search_fields = ('name', 'artist__name')
    list_filter = ['artist', ]
    list_per_page = 50

    def song_artists(self, obj):
        return ", ".join([str(p) for p in obj.artist.all()])


admin.site.register(models.album, AlbumAdmin)


class SongAdmin(admin.ModelAdmin):
    raw_id_fields = ('album', 'artist')
    list_display = ('name', 'song_artists')
    list_filter = ['created_date', 'artist']
    search_fields = ['name', 'artist__name']
    autocomplete_field = ('name',)
    list_per_page = 50

    class Meta:
        model = models.song

    def song_artists(self, obj):
        return ", ".join([str(p) for p in obj.artist.all()])


admin.site.register(models.song, SongAdmin)


class PlaylistSongsAdmin(admin.ModelAdmin):
    raw_id_fields = ('song_id',)
    search_fields = ['name', ]
    autocomplete_field = ('name',)
    list_per_page = 50

    class Meta:
        model = models.song


admin.site.register(models.PlayListSong, PlaylistSongsAdmin)


# qsic's playlists
class PlayListAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name', 'artist__name', 'album__name']
    autocomplete_field = ('name',)
    list_per_page = 50

    class Meta:
        model = models.song


admin.site.register(models.PlayList, PlayListAdmin)


# Followers
class FollowerAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'artist_id')
    list_display = ('user', 'artist_id')
    autocomplete_field = ('name',)
    list_per_page = 50

    class Meta:
        model = models.Follower


admin.site.register(models.Follower, FollowerAdmin)


# Playlist Followers
class PLFollowerAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'playlist')
    list_display = ('user', 'playlist')
    autocomplete_field = ('name',)
    list_per_page = 50

    class Meta:
        model = models.PlaylistFollow


admin.site.register(models.PlaylistFollow, PLFollowerAdmin)


# Favorite
class FavoriteAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'song_id')
    list_display = ('user', 'song_id')
    autocomplete_field = ('name',)
    list_per_page = 50

    class Meta:
        model = models.PlaylistFollow


admin.site.register(models.Favorite, FavoriteAdmin)


# Unmanaged

admin.site.register(models.discount_code)

admin.site.register(models.categories)
