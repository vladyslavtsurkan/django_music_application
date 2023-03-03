from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from music_app.api.views import ArtistViewSet, AlbumViewSet, TrackViewSet

router = DefaultRouter()
router.register('artists', ArtistViewSet)
router.register('albums', AlbumViewSet)
router.register('tracks', TrackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth', obtain_auth_token),
    path("jwt/", TokenObtainPairView.as_view(), name="jwt_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
]
