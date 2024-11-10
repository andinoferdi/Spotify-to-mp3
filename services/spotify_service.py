import os
import spotipy
import spotipy.oauth2 as oauth2
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    auth_manager = oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)

def get_track_info(track_uri):
    spotify_client = get_spotify_client()
    if track_uri.find("https://open.spotify.com/track/") != -1:
        track_uri = track_uri.replace("https://open.spotify.com/track/", "")
    if '?' in track_uri:
        track_uri = track_uri.split('?')[0]

    track_info = spotify_client.track(track_uri)
    return {
        "name": track_info['name'],
        "artist": track_info['artists'][0]['name'],
        "album": track_info['album']['name'],
        "album_cover_url": track_info['album']['images'][0]['url']  # URL gambar album
    }
