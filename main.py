import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the data in  this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(URL)
w_text = response.text
soup = BeautifulSoup(w_text, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://example.com'


sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope="playlist-modify-private")

sp = spotipy.Spotify(auth_manager=sp_oauth)

user_id = sp.current_user()['id']
playlist_name = f"Billboard Hot 100 - {date}"
playlist_description = "A playlist created using Spotipy"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False, description=playlist_description)

track_uris = []

for song in song_names:
    result = sp.search(q=song, type='track', limit=1)
    try:
        track_uri = result['tracks']['items'][0]['uri']
        track_uris.append(track_uri)
    except IndexError:
        print(f"Song '{song}' not found on Spotify.")


if track_uris:
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)
    print(f"Added {len(track_uris)} songs to the playlist: {playlist['name']}")
else:
    print("No songs were added to the playlist.")