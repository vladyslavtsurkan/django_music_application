from spotify_integration.schemas.base import BaseSpotifySchema


class ArtistShortSpotifySchema(BaseSpotifySchema):
    def __init__(self, data: dict):
        self._data = data

        if self._data['type'] != 'artist':
            raise TypeError(f'This is not Spotify Artist -> type: {self._data["type"]}')

    def is_full_information(self) -> bool:
        return bool(self._data.get('genres') is not None)


class ArtistSpotifySchema(ArtistShortSpotifySchema):
    @property
    def image_url(self) -> str:
        self.check_for_detail_data_key('images')
        try:
            return self._data['images'][0]['url']
        except IndexError:
            return ''

    @property
    def genres(self) -> list[str]:
        self.check_for_detail_data_key('genres')
        return self._data['genres']
