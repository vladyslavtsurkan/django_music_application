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


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_filter = ('is_full_record', )
    search_fields = ('name', 'spotify_id', 'album__name', 'artists__name')
    list_display = ('name', 'spotify_id', 'is_full_record')


admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(ExternalID)
admin.site.register(Market)
admin.site.register(Genre)
admin.site.register(AlbumType)
admin.site.register(CopyrightAlbumType)
admin.site.register(CopyrightAlbum)
