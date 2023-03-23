from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ReadOnlyModelViewSet

from music_app.models import Artist, Album, Track
from music_app.api.serializers import (
    ArtistSerializer,
    ArtistDetailSerializer,
    AlbumSerializer,
    AlbumDetailSerializer,
    TrackSerializer,
    TrackDetailSerializer,
)
from music_app.api.filters import (
    ArtistFilterSet,
    TrackFilterSet,
    AlbumFilterSet,
)
from music_app.api.pagination import TrackResultsSetPagination


class ArtistViewSet(ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    filterset_class = ArtistFilterSet

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return ArtistSerializer
        return ArtistDetailSerializer

    def get_queryset(self):
        queryset = self.queryset.all()

        if self.action not in ("list", "create"):
            queryset = queryset.prefetch_related("genres")

        return queryset

    @method_decorator(cache_page(300))
    def list(self, request, *args, **kwargs):
        return super(ArtistViewSet, self).list(request, *args, **kwargs)

    @method_decorator(cache_page(300))
    def retrieve(self, request, *args, **kwargs):
        return super(ArtistViewSet, self).retrieve(request, *args, **kwargs)


class AlbumViewSet(ReadOnlyModelViewSet):
    queryset = Album.objects.all()
    filterset_class = AlbumFilterSet

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return AlbumSerializer
        return AlbumDetailSerializer

    def get_queryset(self):
        queryset = self.queryset.all().select_related(
            'album_type',
        ).prefetch_related(
            'artists', 'available_markets',
        )

        if self.action not in ("list", "create"):
            queryset = queryset.prefetch_related(
                'external_ids', 'copyrights', 'copyrights__copyright_type', 'genres', 'tracks',
                'tracks__available_markets', 'tracks__artists', 'tracks__external_ids', 'tracks__available_markets',
                'external_ids__content_type',
            )

        return queryset

    @method_decorator(cache_page(300))
    def list(self, request, *args, **kwargs):
        return super(AlbumViewSet, self).list(request, *args, **kwargs)

    @method_decorator(cache_page(300))
    def retrieve(self, request, *args, **kwargs):
        return super(AlbumViewSet, self).retrieve(request, *args, **kwargs)


class TrackViewSet(ReadOnlyModelViewSet):
    queryset = Track.objects.all()
    pagination_class = TrackResultsSetPagination
    filterset_class = TrackFilterSet

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return TrackSerializer
        return TrackDetailSerializer

    def get_queryset(self):
        queryset = self.queryset.all().select_related(
            'album', 'album__album_type',
        ).prefetch_related(
            'artists', 'available_markets', 'album__available_markets', 'album__artists',
        )

        if self.action not in ("list", "create"):
            queryset = queryset.prefetch_related(
                'external_ids',
            )

        return queryset

    @method_decorator(cache_page(300))
    def list(self, request, *args, **kwargs):
        return super(TrackViewSet, self).list(request, *args, **kwargs)

    @method_decorator(cache_page(300))
    def retrieve(self, request, *args, **kwargs):
        return super(TrackViewSet, self).retrieve(request, *args, **kwargs)
