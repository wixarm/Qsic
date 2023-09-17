from django.urls import path, include
from core.views import home_view
from .views import RegisterAPIView, LoginAPIView, UserAPIView, RefreshAPIView, LogoutAPIView, ForgotAPIView, \
    ResetAPIView, CategoryList, ArtistList, ArtistByCat, AlbumList, AlbumByArtist, SongList, SongByArtist, SongByAlbum, \
    PlayLists, SongByPlayList, Favorites, Discount, SearchArtist, DeleteFavorite, FavoriteByUserID, SearchAlbum, \
    SearchSong, CheckSubscription, AddFavoriteByUserID, AddSubscription, Followers, FollowerUserID, DeleteFollower, \
    PlaylistFollowerUserID, PlaylistDeleteFollower, PlFollowers

urlpatterns = [
    path('', home_view, name='home'),
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserAPIView.as_view()),
    path('refresh', RefreshAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('forgot', ForgotAPIView.as_view()),
    path('reset', ResetAPIView.as_view()),
    path('categorylist', CategoryList.as_view()),
    path('artistlist', ArtistList.as_view()),
    path('artistlist/<int:pk>/', ArtistByCat),
    path('albumlist', AlbumList.as_view()),
    path('albumbyartist/<int:pk>/', AlbumByArtist),
    path('songlist', SongList.as_view()),
    path('songbyartist/<int:pk>/', SongByArtist),
    path('songbyalbum/<int:pk>/', SongByAlbum),
    path('playlists', PlayLists.as_view()),
    path('plfollowers', PlFollowers.as_view()),
    path('plfollowerbyuser/<int:pk>/', PlaylistFollowerUserID),
    path('pldeletefollower/<int:pk>/', PlaylistDeleteFollower.as_view()),
    path('songbyplaylist/<int:pk>/', SongByPlayList),
    path('favorites', Favorites.as_view()),
    path('favoriteuser/<int:pk>/', FavoriteByUserID),  # Test
    path('addfavorite/<int:pk>/', AddFavoriteByUserID),
    path('deletefavorite/<int:pk>/', DeleteFavorite.as_view()),
    path('discounts', Discount.as_view()),
    path('searchalbum/<str:pk>/', SearchAlbum),
    path('searchartist/<str:pk>/', SearchArtist),
    path('searchsong/<str:pk>/', SearchSong),
    path('checksub/<str:pk>/', CheckSubscription),
    path('addsub/<str:pk>/', AddSubscription),
    path('followers', Followers.as_view()),
    path('followerbyuser/<int:pk>/', FollowerUserID),
    path('deletefollower/<int:pk>/', DeleteFollower.as_view()),
]