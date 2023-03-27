from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from music_app.models import (
    Album,
    CopyrightAlbum,
    Artist,
    Track,
    ExternalID,
    Comment,
)
from music_app.apps import MusicAppConfig


class CustomStringRelatedField(serializers.StringRelatedField):
    def to_internal_value(self, data):
        pass


class AvailableMarketsStringRelatedField(CustomStringRelatedField):
    def to_representation(self, value):
        return str(value.code)


class NameStringRelatedField(CustomStringRelatedField):
    def to_representation(self, value):
        return str(value.name)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    content_type = serializers.ChoiceField(['artist', 'album', 'track'], source='content_type.model')
    creator = serializers.CharField(source='creator.email', read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    children = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'content_type', 'object_id', 'content', 'created_at', 'modified_at', 'creator',
            'parent', 'children',
        ]

    def create(self, validated_data):
        content_type_name = validated_data.pop('content_type')['model']
        content_type = ContentType.objects.get(app_label=MusicAppConfig.name, model=content_type_name)
        comment = Comment.objects.create(content_type=content_type, **validated_data)
        return comment


class ExternalIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalID
        fields = ['name', 'value']


class CopyrightAlbumSerializer(serializers.ModelSerializer):
    copyright_type = NameStringRelatedField(read_only=True)

    class Meta:
        model = CopyrightAlbum
        fields = ['text', 'copyright_type']


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        exclude = ['genres']


class ArtistDetailSerializer(ArtistSerializer):
    genres = NameStringRelatedField(many=True, read_only=True)

    class Meta(ArtistSerializer.Meta):
        exclude = []
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    album_type = NameStringRelatedField(read_only=True)
    artists = ArtistSerializer(read_only=True, many=True)
    available_markets = AvailableMarketsStringRelatedField(many=True, read_only=True)

    class Meta:
        model = Album
        exclude = ['copyrights', 'genres']


class AlbumTrackDetailSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(read_only=True, many=True)
    available_markets = AvailableMarketsStringRelatedField(many=True, read_only=True)
    external_ids = ExternalIDSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        exclude = ['album']


class AlbumDetailSerializer(AlbumSerializer):
    copyrights = CopyrightAlbumSerializer(read_only=True, many=True)
    genres = NameStringRelatedField(many=True, read_only=True)
    external_ids = ExternalIDSerializer(many=True, read_only=True)
    tracks = AlbumTrackDetailSerializer(many=True, read_only=True)

    class Meta(AlbumSerializer.Meta):
        exclude = []
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)
    artists = ArtistSerializer(read_only=True, many=True)
    available_markets = AvailableMarketsStringRelatedField(many=True, read_only=True)

    class Meta:
        model = Track
        fields = '__all__'


class TrackDetailSerializer(TrackSerializer):
    external_ids = ExternalIDSerializer(many=True, read_only=True)
