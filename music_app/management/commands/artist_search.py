from django.core.management.base import BaseCommand

from music_app.services.spotify_integration import (
    search_artists_by_query,
    save_artists_to_database,
)


class Command(BaseCommand):
    help = "Search Spotify API and populates the database with results"

    def add_arguments(self, parser):
        parser.add_argument("search", nargs="+")

    def handle(self, *args, **options):
        search = " ".join(options["search"])
        artists_list = search_artists_by_query(search)
        save_artists_to_database(artists_list)
