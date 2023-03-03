from rest_framework.viewsets import ReadOnlyModelViewSet

from music_app.api.serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from music_app.models import Artist, Album, Track
from music_app.api.filters import ArtistFilterSet


class ArtistViewSet(ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_class = ArtistFilterSet


class AlbumViewSet(ReadOnlyModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class TrackViewSet(ReadOnlyModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
