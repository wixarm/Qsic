from rest_framework.serializers import ModelSerializer
from .models import User, PlayList, Favorite, discount_code, Follower, PlaylistFollow, PlayListSong
from .models import categories, artist, album, song
from rest_framework import serializers


# serializer: when we create a user, the user wo go to views.py and we need to return the user as an object and the
# object will convert to a json object
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # what will happen after creation the user - extracting and making HASH the password and remove of response json
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # create user without password
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class categorySerializer(ModelSerializer):
    class Meta:
        model = categories
        fields = ['id', 'name', 'cover']


class artistSerializer(ModelSerializer):
    class Meta:
        model = artist
        fields = "__all__"


class albumSerializer(ModelSerializer):
    class Meta:
        model = album
        fields = "__all__"


class songSerializer(ModelSerializer):
    class Meta:
        model = song
        fields = "__all__"


class playlistSerializer(ModelSerializer):
    class Meta:
        model = PlayList
        fields = "__all__"


class songByPlaylistSerializer(ModelSerializer):
    class Meta:
        model = PlayListSong
        fields = "__all__"


class playlistFollowersSerializer(ModelSerializer):
    class Meta:
        model = PlaylistFollow
        fields = "__all__"


class favoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"


class discountSerializer(ModelSerializer):
    class Meta:
        model = discount_code
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'exp_sub']


class followerSerializer(ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"


