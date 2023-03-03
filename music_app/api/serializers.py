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
)


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
        fields = ['id', 'text']


class ArtistSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    album_type = AlbumTypeSerializer(read_only=True)
    copyrights = CopyrightAlbumSerializer(read_only=True, many=True)
    artists = ArtistSerializer(read_only=True, many=True)
    genres = GenreSerializer(many=True, read_only=True)
    available_markets = MarketSerializer(many=True, read_only=True)
    external_ids = ExternalIDSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)
    artists = ArtistSerializer(read_only=True, many=True)
    available_markets = MarketSerializer(many=True, read_only=True)
    external_ids = ExternalIDSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        fields = '__all__'
