from django.core.management.base import BaseCommand

from music_app.services.spotify_integration import (
    get_not_is_full_record_spotify_ids_by_type,
    full_model_by_type_and_spotify_ids,
)


class Command(BaseCommand):
    help = "Full all Album models if is_full_record attribute is False"

    def handle(self, *args, **options):
        album_spotify_ids_list = get_not_is_full_record_spotify_ids_by_type('album')
        full_model_by_type_and_spotify_ids('album', album_spotify_ids_list)
