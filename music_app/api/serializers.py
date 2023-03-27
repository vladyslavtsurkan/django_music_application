from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from music_app.models import (
    Album,
    AlbumType,
    CopyrightAlbumType,
    CopyrightAlbum,
    Artist,
    Track,
    Market,
    ExternalID,
    Genre,
    Comment,
)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    content_type = serializers.ChoiceField(['artist', 'album', 'track'], source='content_type.model')
    creator = serializers.CharField(source='creator.email', read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())

    class Meta:
        model = Comment
        fields = [
            'id', 'content_type', 'object_id', 'content', 'created_at', 'modified_at', 'creator',
            'parent',
        ]

    def create(self, validated_data):
        content_type_name = validated_data.pop('content_type')['model']
        print(content_type_name)
        content_type = ContentType.objects.get(app_label='music_app', model=content_type_name)
        comment = Comment.objects.create(content_type=content_type, **validated_data)
        return comment


class ExternalIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalID
        fields = ['id', 'name', 'value']


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AlbumTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumType
        fields = '__all__'


class CopyrightAlbumTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CopyrightAlbumType
        fields = '__all__'


class CopyrightAlbumSerializer(serializers.ModelSerializer):
    copyright_type = CopyrightAlbumTypeSerializer(read_only=True)

    class Meta:
        model = CopyrightAlbum
        fields = ['id', 'text', 'copyright_type']


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        exclude = ['genres']


class ArtistDetailSerializer(ArtistSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta(ArtistSerializer.Meta):
        exclude = []
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    album_type = AlbumTypeSerializer(read_only=True)
    artists = ArtistSerializer(read_only=True, many=True)
    available_markets = MarketSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        exclude = ['copyrights', 'genres']


class AlbumTrackDetailSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(read_only=True, many=True)
    available_markets = MarketSerializer(many=True, read_only=True)
    external_ids = ExternalIDSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        # fields = '__all__'
        exclude = ['album']


class AlbumDetailSerializer(AlbumSerializer):
    copyrights = CopyrightAlbumSerializer(read_only=True, many=True)
    genres = GenreSerializer(many=True, read_only=True)
    external_ids = ExternalIDSerializer(many=True, read_only=True)
    tracks = AlbumTrackDetailSerializer(many=True, read_only=True)

    class Meta(AlbumSerializer.Meta):
        exclude = []
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)
    artists = ArtistSerializer(read_only=True, many=True)
    available_markets = MarketSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        fields = '__all__'


class TrackDetailSerializer(TrackSerializer):
    external_ids = ExternalIDSerializer(many=True, read_only=True)
