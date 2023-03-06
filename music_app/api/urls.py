from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from music_app.api.views import ArtistViewSet, AlbumViewSet, TrackViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Open Spotify API",
        default_version="v1",
        description="API for Spotify",
    ),
    url=f"http://127.0.0.1:8000/api/v1/",
    public=True,
)

router = DefaultRouter()
router.register('artists', ArtistViewSet)
router.register('albums', AlbumViewSet)
router.register('tracks', TrackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth', obtain_auth_token),
    path("jwt/", TokenObtainPairView.as_view(), name="jwt_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
