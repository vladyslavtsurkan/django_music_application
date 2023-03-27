from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters

from music_app.models import Artist, Track, Album
from music_app.apps import MusicAppConfig

_content_types_id = {
    'artist': ContentType.objects.get(app_label=MusicAppConfig.name, model='artist').id,
    'album': ContentType.objects.get(app_label=MusicAppConfig.name, model='album').id,
    'track': ContentType.objects.get(app_label=MusicAppConfig.name, model='track').id,
}


class BaseSpotifyFilterSet(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Name',
    )
    spotify_id = filters.CharFilter(
        field_name='spotify_id',
        lookup_expr='exact',
        label='Spotify ID',
    )
    spotify_uri = filters.CharFilter(
        field_name='spotify_uri',
        lookup_expr='exact',
        label='Spotify URI',
    )


class ArtistFilterSet(BaseSpotifyFilterSet):
    class Meta:
        model = Artist
        fields = []


class TrackFilterSet(BaseSpotifyFilterSet):
    class Meta:
        model = Track
        fields = []


class AlbumFilterSet(BaseSpotifyFilterSet):
    class Meta:
        model = Album
        fields = []


class CommentFilterSet(filters.FilterSet):
    creator = filters.NumberFilter(
        field_name='creator_id',
        lookup_expr='exact',
        label='Creator ID',
    )
    content_type = filters.ChoiceFilter(
        choices=[
            (_content_types_id['artist'], 'artist'),
            (_content_types_id['album'], 'album'),
            (_content_types_id['track'], 'track')
        ],
        field_name='content_type',
        lookup_expr='exact',
        label='Type of model'
    )
