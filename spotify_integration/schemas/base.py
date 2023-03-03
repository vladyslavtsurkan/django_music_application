from abc import ABC, abstractmethod


class BaseSpotifySchema(ABC):
    __slots__ = ['_data']

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def is_full_information(self):
        pass

    def check_for_detail_data_key(self, key) -> None:
        """Some keys are only in the detail response, raise an
        exception if the key is not found."""

        if key not in self._data:
            raise AttributeError(
                f"{key} is not in data, please make sure this is a detail response."
            )

    @property
    def name(self) -> str:
        self.check_for_detail_data_key('name')
        return self._data['name']

    @property
    def spotify_id(self) -> str:
        self.check_for_detail_data_key('id')
        return self._data['id']

    @property
    def spotify_uri(self) -> str:
        self.check_for_detail_data_key('uri')
        return self._data['uri']
