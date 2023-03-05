from django_filters import rest_framework as filters

from music_app.models import Artist, Track, Album


class BaseSpotifyFilterSet(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Artist name',
    )
    spotify_id = filters.CharFilter(
        field_name='spotify_id',
        lookup_expr='exact',
        label='Artist Spotify ID',
    )
    spotify_uri = filters.CharFilter(
        field_name='spotify_uri',
        lookup_expr='exact',
        label='Artist Spotify URI',
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
