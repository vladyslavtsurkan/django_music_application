from datetime import date

from spotify_integration.schemas.base import BaseSpotifySchema


class AlbumShortSpotifySchema(BaseSpotifySchema):
    def __init__(self, data: dict):
        self._data = data

        if self._data['type'] != 'album':
            raise TypeError(f'This is not Spotify Album -> type: {self._data["type"]}')

    @property
    def image_url(self) -> str:
        self.check_for_detail_data_key('images')
        return self._data['images'][0]['url']

    @property
    def album_type(self) -> str:
        self.check_for_detail_data_key('album_type')
        return self._data['album_type']

    @property
    def available_markets(self) -> list[str]:
        self.check_for_detail_data_key('available_markets')
        return self._data['available_markets']

    @property
    def artists_spotify_ids(self) -> list[str]:
        self.check_for_detail_data_key('artists')
        artists = self._data['artists']

        return [artist['id'] for artist in artists]

    @property
    def release_date(self) -> date:
        self.check_for_detail_data_key('release_date')
        release_date_list = self._data['release_date'].split('-')

        match release_date_list:
            case year_str, month_str, day_str:
                release_date = date(
                    year=int(year_str),
                    month=int(month_str),
                    day=int(day_str),
                )
            case year_str, month_str:
                release_date = date(
                    year=int(year_str),
                    month=int(month_str),
                    day=1,
                )
            case year_str:
                release_date = date(
                    year=int(year_str),
                    month=1,
                    day=1,
                )

        return release_date


class AlbumSpotifySchema(AlbumShortSpotifySchema):
    @property
    def external_ids(self) -> dict[str, str]:
        self.check_for_detail_data_key('external_ids')
        return self._data['external_ids']

    @property
    def copyrights(self) -> list[dict[str, str]]:
        self.check_for_detail_data_key('copyrights')
        return self._data['copyrights']

    @property
    def genres(self) -> list[str]:
        self.check_for_detail_data_key('genres')
        return self._data['genres']