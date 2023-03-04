from rest_framework.viewsets import ReadOnlyModelViewSet

from music_app.models import Artist, Album, Track
from music_app.api.serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from music_app.api.filters import ArtistFilterSet


class ArtistViewSet(ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filterset_class = ArtistFilterSet

    def get_queryset(self):
        return self.queryset.all().prefetch_related('genres')


class AlbumViewSet(ReadOnlyModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_queryset(self):
        return self.queryset.all().select_related(
            'album_type',
        ).prefetch_related(
            'external_ids', 'copyrights', 'artists', 'artists__genres', 'genres',
            'available_markets', 'copyrights__copyright_type'
        )


class TrackViewSet(ReadOnlyModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def get_queryset(self):
        return self.queryset.all().select_related(
            'album', 'album__album_type'
        ).prefetch_related(
            'artists', 'available_markets',
            'external_ids', 'album__available_markets',
            'album__artists', 'album__genres', 'album__artists__genres',
            'album__external_ids', 'artists__genres', 'album__copyrights',
            'album__copyrights__copyright_type',
        )
