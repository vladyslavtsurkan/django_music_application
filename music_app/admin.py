from django.contrib import admin

from music_app.models import (
    Track,
    Artist,
    Album,
    ExternalID,
    Market,
    Genre,
    AlbumType,
    CopyrightAlbumType,
    CopyrightAlbum
)

admin.site.register(Track)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(ExternalID)
admin.site.register(Market)
admin.site.register(Genre)
admin.site.register(AlbumType)
admin.site.register(CopyrightAlbumType)
admin.site.register(CopyrightAlbum)
