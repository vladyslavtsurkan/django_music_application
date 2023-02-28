import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

# artist_rammstein = sp.artist('6wWVKhxIU2cEi0K81v7HvP')
album_mutter = sp.album('https://open.spotify.com/album/1CtTTpKbHU8KbHRB4LmBbv?si=cLx2YFy6QBioh75X2C0OxQ')
# album_mutter = sp.album('https://open.spotify.com/album/4POwouNbBP807ciWs9WIfM?si=hF9ku8N-QtqAJHZgWB4bVQ')
# track_ich_will = sp.track('https://open.spotify.com/track/3X0K6fII7VIwL1URPrp8Ko?si=7ba106100b3e4608')

# pprint(artist_rammstein)
pprint(album_mutter)
# pprint(track_ich_will)