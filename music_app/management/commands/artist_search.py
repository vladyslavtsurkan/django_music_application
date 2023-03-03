from django.core.management.base import BaseCommand

from music_app.services.spotify_integration import search_and_save_artist


class Command(BaseCommand):
    help = "Search Spotify API and populates the database with results"

    def add_arguments(self, parser):
        parser.add_argument("search", nargs="+")

    def handle(self, *args, **options):
        search = " ".join(options["search"])
        search_and_save_artist(search)
