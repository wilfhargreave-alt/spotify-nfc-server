from flask import Flask
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-playback-state user-modify-playback-state"
))

albums = {
    "album_01": "spotify:album:1A2GTWGtFfWp7KSQTwWOyo",
    "album_02": "spotify:album:4aawyAB9vmqN3uQ7FjRGTy"
}

@app.route("/play/<album_id>")
def play_album(album_id):

    if album_id in albums:
        sp.start_playback(context_uri=albums[album_id])
        return f"Playing {album_id}"

    return "Album not found"

app.run(host="0.0.0.0", port=5000)