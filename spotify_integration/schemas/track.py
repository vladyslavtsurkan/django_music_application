from spotify_integration.schemas.base import BaseSpotifySchema


class TrackShortSpotifySchema(BaseSpotifySchema):
    def __init__(self, data: dict):
        self._data = data

        if self._data['type'] != 'track':
            raise TypeError(f'This is not Spotify Track -> type: {self._data["type"]}')

    def is_full_information(self) -> bool:
        return bool(self._data.get('album'))

    @property
    def track_number_of_album(self) -> int | None:
        return self._data.get('track_number')

    @property
    def is_explicit(self) -> bool:
        self.check_for_detail_data_key('explicit')
        return self._data['explicit']

    @property
    def duration_ms(self) -> int:
        self.check_for_detail_data_key('duration_ms')
        return self._data['duration_ms']

    @property
    def available_markets(self) -> list[str]:
        self.check_for_detail_data_key('available_markets')
        return self._data['available_markets']

    @property
    def artists_spotify_ids(self) -> list[str]:
        self.check_for_detail_data_key('artists')
        artists = self._data['artists']

        return [artist['id'] for artist in artists]


class TrackSpotifySchema(TrackShortSpotifySchema):
    @property
    def external_ids(self) -> dict:
        self.check_for_detail_data_key('external_ids')
        return self._data['external_ids']

    @property
    def album_spotify_id(self) -> str:
        self.check_for_detail_data_key('album')
        return self._data['album']['id']
