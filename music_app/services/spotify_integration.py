import logging
from typing import Generator

from music_app.models import Artist, Genre, Track, Album
from spotify_integration import (
    ArtistShortSpotifySchema,
    ArtistSpotifySchema,
    AlbumShortSpotifySchema,
    AlbumSpotifySchema,
    TrackShortSpotifySchema,
    TrackSpotifySchema,
    client_spotify
)

logger = logging.getLogger(__name__)


def get_or_create_genres(genre_names_list: list[str]) -> Generator:
    for genre_name in genre_names_list:
        genre, created = Genre.objects.get_or_create(name=genre_name)
        yield genre


def search_artists_by_query(query: str) -> list[dict]:
    response = client_spotify.search(q=query, limit=10, type='artist')
    artists = response.get('artists', {}).get('items', [])

    return artists


def save_artists_to_database(artists_list: list[dict]) -> None:
    for artist in artists_list:
        artist_by_schema = ArtistSpotifySchema(artist)

        artist_dict = {
            'name': artist_by_schema.name,
            'spotify_id': artist_by_schema.spotify_id,
            'spotify_uri': artist_by_schema.spotify_uri,
        }

        artist_instance, created = Artist.objects.get_or_create(**artist_dict)

        if not artist_instance.is_full_record and artist_by_schema.is_full_information():
            artist_instance.is_full_record = True
            artist_instance.artist_image_url = artist_by_schema.image_url
            artist_instance.save()
            artist_instance.genres.add(*get_or_create_genres(artist_by_schema.genres))
