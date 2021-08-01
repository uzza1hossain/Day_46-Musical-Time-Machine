import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"
spotify_client_id = os.environ["SPOTIFY_CLIENT_ID"]
spotify_client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]

# Scraping Top 100 Songs from Selected date
travel_date = input("Which year do you want to travel to? Type date in this format YYYY-MM-DD: ")
soup = BeautifulSoup((requests.get(f"{URL}{travel_date}")).content, "html.parser")
top_100_song = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_names = [song.getText() for song in top_100_song]

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        cache_path=".cache"
    )
)
user_id = sp.current_user()["id"]

# Searching songs using title
song_uris = []
year = travel_date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pass
        #print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist
my_play_list = sp.user_playlist_create(user=user_id, name=f"{travel_date} Billboard 100", public=False)

# Adding songs into playlist
sp.playlist_add_items(playlist_id=my_play_list["id"], items=song_uris)
print(my_play_list)
