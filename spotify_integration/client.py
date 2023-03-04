from typing import Literal

import spotipy
# from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials


# auth_manager = SpotifyClientCredentials()
# client_spotify = spotipy.Spotify(auth_manager=auth_manager)

# search = client_spotify.search('rammstein', limit=20, type='album')
# artist_rammstein = client_spotify.artist('6wWVKhxIU2cEi0K81v7HvP')
# album_mutter = client_spotify.album('https://open.spotify.com/album/1CtTTpKbHU8KbHRB4LmBbv?si=cLx2YFy6QBioh75X2C0OxQ')
#### album_mutter = sp.album('https://open.spotify.com/album/4POwouNbBP807ciWs9WIfM?si=hF9ku8N-QtqAJHZgWB4bVQ')
# track_ich_will = client_spotify.track('https://open.spotify.com/track/3X0K6fII7VIwL1URPrp8Ko?si=7ba106100b3e4608')

# pprint(artist_rammstein)
# pprint(album_mutter)
# pprint(track_ich_will)
# pprint(search)


class SpotifyClient:
    def __init__(self):
        self.__auth_manager = SpotifyClientCredentials()
        self.__client_spotify = spotipy.Spotify(auth_manager=self.__auth_manager)

    def search(self, *args, **kwargs):
        return self.__client_spotify.search(*args, **kwargs)

    def get_artist_by_spotify_id_or_uri(self, spotify_id_or_uri: str) -> dict:
        return self.__client_spotify.artist(spotify_id_or_uri)

    def get_track_by_spotify_id_or_uri(self, spotify_id_or_uri: str) -> dict:
        return self.__client_spotify.track(spotify_id_or_uri)

    def get_album_by_spotify_id_or_uri(self, spotify_id_or_uri: str) -> dict:
        return self.__client_spotify.album(spotify_id_or_uri)

    def get_object_by_type_and_spotify_id_or_uri(
            self,
            type_str: Literal['artist', 'track', 'album'],
            spotify_id_or_uri: str
    ) -> dict:
        match type_str:
            case 'artist':
                result = self.get_artist_by_spotify_id_or_uri(spotify_id_or_uri)
            case 'album':
                result = self.get_album_by_spotify_id_or_uri(spotify_id_or_uri)
            case 'track':
                result = self.get_track_by_spotify_id_or_uri(spotify_id_or_uri)
            case _:
                raise ValueError("Unknown type")

        return result
