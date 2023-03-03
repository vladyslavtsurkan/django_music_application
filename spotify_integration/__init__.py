from spotify_integration.schemas.artist import ArtistShortSpotifySchema, ArtistSpotifySchema
from spotify_integration.schemas.album import AlbumShortSpotifySchema, AlbumSpotifySchema
from spotify_integration.schemas.track import TrackShortSpotifySchema, TrackSpotifySchema
from spotify_integration.client import client_spotify

__all__ = [
    'client_spotify',
    'AlbumShortSpotifySchema',
    'AlbumSpotifySchema',
    'TrackShortSpotifySchema',
    'TrackSpotifySchema',
    'ArtistShortSpotifySchema',
    'ArtistSpotifySchema'
]
