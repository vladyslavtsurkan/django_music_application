import logging
from time import sleep
from typing import Generator, Sequence, Literal
from requests.exceptions import Timeout

from django.contrib.contenttypes.models import ContentType

from music_app.models import (
    Artist,
    Genre,
    Track,
    Album,
    AlbumType,
    CopyrightAlbumType,
    CopyrightAlbum,
    Market,
    ExternalID,
)
from spotify_integration import (
    ArtistSpotifySchema,
    AlbumSpotifySchema,
    TrackSpotifySchema,
    SpotifyClient,
)

logger = logging.getLogger(__name__)
client_spotify = SpotifyClient()

LIMIT_ARTIST_OBJECTS = 50
LIMIT_ALBUM_OBJECTS = 50
LIMIT_TRACK_OBJECTS = 50

_type_to_model = {
    'artist': Artist,
    'album': Album,
    'track': Track,
}


def get_or_create_genres(genre_names_list: list[str]) -> Generator:
    for genre_name in genre_names_list:
        genre, created = Genre.objects.get_or_create(name=genre_name)
        yield genre


def get_or_create_markets(market_codes_list: list[str]) -> Generator:
    for market_code in market_codes_list:
        market, created = Market.objects.get_or_create(code=market_code)
        yield market


def get_or_create_copyrights(copyright_list: list[dict]) -> Generator:
    for copyright_dict in copyright_list:
        copyright_type, created = CopyrightAlbumType.objects.get_or_create(
            name=copyright_dict.get('type')
        )
        copyright_instance, created = CopyrightAlbum.objects.get_or_create(
            copyright_type=copyright_type,
            text=copyright_dict.get('text')
        )
        yield copyright_instance


def get_or_create_external_ids(external_ids_dict: dict, relation_object: Track | Album):
    for name, value in external_ids_dict.items():
        relation_object_type = ContentType.objects.get(
            app_label=__name__.split('.')[0],
            model=relation_object.__class__.__name__.lower()
        )
        ExternalID.objects.get_or_create(
            name=name,
            value=value,
            object_id=relation_object.id,
            content_type=relation_object_type,
        )


def search_artists_by_query(query: str) -> list[dict]:
    response = client_spotify.search(q=query, limit=LIMIT_ARTIST_OBJECTS, type='artist')
    artists = response.get('artists', {}).get('items', [])

    return artists


def save_artists_to_database(artist_list: list[dict]) -> list[Artist]:
    artist_instances = []

    for artist in artist_list:
        artist_instance = save_artist_to_database(artist)
        artist_instances.append(artist_instance)

    return artist_instances


def save_artist_to_database(artist_dict: dict) -> Artist:
    artist_by_schema = ArtistSpotifySchema(artist_dict)

    artist_dict_for_save = {
        'name': artist_by_schema.name,
        'spotify_id': artist_by_schema.spotify_id,
        'spotify_uri': artist_by_schema.spotify_uri,
    }

    artist_instance, created = Artist.objects.get_or_create(**artist_dict_for_save)

    if created:
        logger.info(
            f'Artist instance with name {artist_by_schema.name} will saved to database '
            f'(Spotify ID - {artist_by_schema.spotify_id}).'
        )

    if not artist_instance.is_full_record and artist_by_schema.is_full_information():
        artist_instance.is_full_record = True
        artist_instance.artist_image_url = artist_by_schema.image_url
        artist_instance.save()
        artist_instance.genres.add(*get_or_create_genres(artist_by_schema.genres))

    return artist_instance


def search_albums_by_query(query: str) -> list[dict]:
    response = client_spotify.search(q=query, limit=LIMIT_ALBUM_OBJECTS, type='album')
    albums = response.get('albums', {}).get('items', [])

    return albums


def save_albums_to_database(album_list: list[dict]) -> list[Album]:
    album_instances = []

    for album in album_list:
        album_instance = save_album_to_database(album)
        album_instances.append(album_instance)

    return album_instances


# don't work
def save_album_to_database(album_dict: dict) -> Album:
    album_by_schema = AlbumSpotifySchema(album_dict)

    album_type, created = AlbumType.objects.get_or_create(name=album_by_schema.album_type)

    album_dict_for_save = {
        'name': album_by_schema.name,
        'spotify_id': album_by_schema.spotify_id,
        'spotify_uri': album_by_schema.spotify_uri,
        'album_image_url': album_by_schema.image_url,
        'album_type': album_type,
        'release_date': album_by_schema.release_date,
    }

    album_instance, created = Album.objects.get_or_create(**album_dict_for_save)

    album_instance.available_markets.add(
        *get_or_create_markets(album_by_schema.available_markets)
    )
    album_artists = save_artists_to_database(album_by_schema.artist_dicts)
    album_instance.artists.add(*album_artists)

    if created:
        logger.info(
            f'Album instance with name {album_by_schema.name} will saved to database '
            f'(Spotify ID - {album_by_schema.spotify_id}).'
        )

    if not album_instance.is_full_record and album_by_schema.is_full_information():
        album_instance.is_full_record = True
        album_instance.save()
        album_instance.copyrights.add(*get_or_create_copyrights(album_by_schema.copyrights))
        album_instance.genres.add(*get_or_create_genres(album_by_schema.genres))
        album_tracks = save_tracks_to_database(album_by_schema.tracks)
        album_instance.tracks.add(*album_tracks)
        album_instance.genres.add(*get_or_create_genres(album_by_schema.genres))
        get_or_create_external_ids(
            album_by_schema.external_ids,
            album_instance
        )

    return album_instance


def search_tracks_by_query(query: str) -> list[dict]:
    response = client_spotify.search(q=query, limit=LIMIT_TRACK_OBJECTS, type='track')
    tracks = response.get('tracks', {}).get('items', [])

    return tracks


def save_tracks_to_database(track_list: list[dict]) -> list[Track]:
    track_instances = []

    for track in track_list:
        track_instance = save_track_to_database(track)
        track_instances.append(track_instance)

    return track_instances


def save_track_to_database(track_dict: dict) -> Track:
    track_by_schema = TrackSpotifySchema(track_dict)

    track_dict_for_save = {
        'name': track_by_schema.name,
        'spotify_id': track_by_schema.spotify_id,
        'spotify_uri': track_by_schema.spotify_uri,
        'is_explicit': track_by_schema.is_explicit,
        'track_number_of_album': track_by_schema.track_number_of_album,
        'duration_ms': track_by_schema.duration_ms,
    }

    track_instance, created = Track.objects.get_or_create(**track_dict_for_save)

    track_instance.available_markets.add(
        *get_or_create_markets(track_by_schema.available_markets)
    )
    track_artists = save_artists_to_database(track_by_schema.artist_dicts)
    track_instance.artists.add(*track_artists)

    if created:
        logger.info(
            f'Track instance with name {track_by_schema.name} will saved to database '
            f'(Spotify ID - {track_by_schema.spotify_id}).'
        )

    if not track_instance.is_full_record and track_by_schema.is_full_information():
        get_or_create_external_ids(
            track_by_schema.external_ids,
            track_instance
        )
        album_for_track = save_album_to_database(track_by_schema.album_dict)
        track_instance.album = album_for_track
        track_instance.is_full_record = True
        track_instance.save()

    return track_instance


def get_not_is_full_record_spotify_ids_by_type(
        type_str: Literal["artist", "track", "album"]
) -> Sequence[str]:
    spotify_ids = _type_to_model[type_str].objects.all().filter(
        is_full_record=False
    ).values_list('spotify_id', flat=True)

    return spotify_ids


def full_model_by_type_and_spotify_ids(
        type_str:  Literal["artist", "track", "album"],
        spotify_ids_list: Sequence[str]
) -> None:
    for spotify_id in spotify_ids_list:
        try:
            object_dict = client_spotify.get_object_by_type_and_spotify_id_or_uri(type_str, spotify_id)
            match type_str:
                case 'artist':
                    save_artist_to_database(object_dict)
                case 'album':
                    save_album_to_database(object_dict)
                case 'track':
                    save_track_to_database(object_dict)
                case _:
                    raise ValueError("Unknown type")

            sleep(0.1)
        except Timeout:
            sleep(5)
