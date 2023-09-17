import datetime
import random
import string
from rest_framework import generics, permissions, viewsets
from django.core.mail import send_mail
from rest_framework.generics import UpdateAPIView
from django.shortcuts import render, get_list_or_404
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from rest_framework import exceptions
from .models import categories, artist, discount_code, PlayListSong, song, album, PlayList, Favorite, \
    Follower, PlaylistFollow
from core.authentication import create_access_token, JWTAuthentication, create_refresh_token, decode_refresh_token
from core.models import User, UserToken, Reset
from core.serializers import UserSerializer, categorySerializer, artistSerializer, albumSerializer, songSerializer, \
    playlistSerializer, favoriteSerializer, discountSerializer, UserSubscriptionSerializer, followerSerializer, \
    playlistFollowersSerializer, songByPlaylistSerializer


def home_view(request,*args, **kwargs):
    return render(request, template_name="index.html")

class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords are not match!')  # validation
        # create User
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)  # validation
        serializer.save()
        return Response(serializer.data)  # return user as a json object


# login
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid Credentials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid Credentials')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        UserToken.objects.create(
            user_id=user.id,
            token=refresh_token,
            expired_at=datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        )

        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token
        }
        return response


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# get token from cookie
class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        if not UserToken.objects.filter(
                user_id=id,
                token=refresh_token,
                expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).exists():
            raise exceptions.AuthenticationFailed('unauthenticated')

        access_token = create_access_token(id)

        return Response({
            'token': access_token
        })


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        UserToken.objects.filter(token=refresh_token).delete()

        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message': 'success'
        }

        return response


class ForgotAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

        Reset.objects.create(
            email=email,
            token=token
        )

        url = 'http//localhost:5005/reset/' + token

        send_mail(
            subject='Reset Your Password',
            message='Click <a href="%s">here</a> to reset your password' % url,
            from_email='from@example.com',
            recipient_list=[email]
        )

        return Response({
            'message': 'success! check your email'
        })


class ResetAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords are not match!')  # validation

        reset_password = Reset.objects.filter(token=data['token']).first()

        if not reset_password:
            raise exceptions.APIException('Invalid link!')

        user = User.objects.filter(email=reset_password.email).first()

        if not user:
            raise exceptions.APIException('User not found!')

        user.set_password(data['password'])
        user.save()

        return Response({
            'message': 'Password Changed!'
        })


class CategoryList(generics.ListAPIView):
    queryset = categories.objects.all()
    serializer_class = categorySerializer


# Artist API
class ArtistList(generics.ListAPIView):
    queryset = artist.objects.all()
    serializer_class = artistSerializer


@api_view(['GET'])
def ArtistByCat(request, pk):
    artists = artist.objects.filter(category=pk)
    artist_serializer = artistSerializer(artists, many=True)
    return Response(artist_serializer.data)


# Album API
class AlbumList(generics.ListAPIView):
    queryset = album.objects.all()
    serializer_class = albumSerializer


@api_view(['GET'])
def AlbumByArtist(request, pk):
    albums = album.objects.filter(artist=pk)
    album_Serializer = albumSerializer(albums, many=True)
    return Response(album_Serializer.data)


# Song API
class SongList(generics.ListAPIView):
    queryset = song.objects.filter(status="published")
    serializer_class = albumSerializer


@api_view(['GET'])
def SongByArtist(request, pk):
    albums = song.objects.filter(artist=pk)
    song_Serializer = songSerializer(albums, many=True)
    return Response(song_Serializer.data)


@api_view(['GET'])
def SongByAlbum(request, pk):
    songs = song.objects.filter(album=pk)
    song_Serializer = songSerializer(songs, many=True)
    return Response(song_Serializer.data)


# PlayList API
class PlayLists(generics.ListAPIView):
    queryset = PlayList.objects.all()
    serializer_class = playlistSerializer


@api_view(['GET'])
def SongByPlayList(request, pk):
    songs = PlayListSong.objects.filter(id=pk)
    song_Serializer = songByPlaylistSerializer(songs, many=True)
    return Response(song_Serializer.data)


# Favorites API
class Favorites(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Favorite.objects.all()
    serializer_class = favoriteSerializer


# Test ---------------------
@api_view(['POST'])
def AddFavoriteByUserID(request, pk):
    songs = Favorite.objects.filter(user=pk)
    song_Serializer = favoriteSerializer(songs, many=True)
    return Response(song_Serializer.data)


@api_view(['GET'])
def FavoriteByUserID(request, pk):
    songs = Favorite.objects.filter(user=pk)
    song_Serializer = favoriteSerializer(songs, many=True)
    return Response(song_Serializer.data)


class DeleteFavorite(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Favorite.objects.all()
    serializer_class = favoriteSerializer

    def perform_create(self, serializer):
        serializer.save(id=self.request.user)


# Discount API
class Discount(generics.ListAPIView):
    queryset = discount_code.objects.all()
    serializer_class = discountSerializer


# Search
@api_view(['GET'])
def SearchAlbum(request, pk):
    albums = album.objects.filter(name__contains=pk)
    album_Serializer = albumSerializer(albums, many=True)
    return Response(album_Serializer.data)


@api_view(['GET'])
def SearchArtist(request, pk):
    songs = artist.objects.filter(name__contains=pk)
    songtags = artist.objects.filter(tags__contains=pk)
    song_Serializer = artistSerializer(songs, many=True)
    songtags_Serializer = artistSerializer(songtags, many=True)
    return Response({"name": song_Serializer.data,
                     "tags": songtags_Serializer.data})


@api_view(['GET'])
def SearchSong(request, pk):
    songs = song.objects.filter(name__contains=pk)
    songtags = song.objects.filter(tags__contains=pk)
    song_Serializer = songSerializer(songs, many=True)
    songtags_Serializer = songSerializer(songtags, many=True)
    return Response({"name": song_Serializer.data,
                     "tags": songtags_Serializer.data})


# Subscription
@api_view(['GET'])
def CheckSubscription(request, pk):
    usersub = User.objects.filter(id=pk)
    song_Serializer = UserSubscriptionSerializer(usersub, many=True)

    return Response(song_Serializer.data)


@api_view(['GET', 'POST'])
def AddSubscription(request, pk):
    usersub = User.objects.get(id=pk)
    song_Serializer = UserSubscriptionSerializer(instance=usersub, data=request.data)

    if song_Serializer.is_valid():
        song_Serializer.save()
    return Response(song_Serializer.data)


# Follow
class Followers(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Follower.objects.all()
    serializer_class = followerSerializer


@api_view(['GET'])
def FollowerUserID(request, pk):
    follower = Follower.objects.filter(user=pk)
    follow_Serializer = followerSerializer(follower, many=True)
    return Response(follow_Serializer.data)


class DeleteFollower(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Follower.objects.all()
    serializer_class = followerSerializer

    def perform_create(self, serializer):
        serializer.save(id=self.request.user)


# Playlist Follows
class PlFollowers(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PlaylistFollow.objects.all()
    serializer_class = playlistFollowersSerializer


@api_view(['GET'])
def PlaylistFollowerUserID(request, pk):
    follower = PlaylistFollow.objects.filter(user=pk)
    follow_Serializer = playlistFollowersSerializer(follower, many=True)
    return Response(follow_Serializer.data)


class PlaylistDeleteFollower(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PlaylistFollow.objects.all()
    serializer_class = playlistFollowersSerializer

    def perform_create(self, serializer):
        serializer.save(id=self.request.user)