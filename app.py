from flask import Flask, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="user-modify-playback-state user-read-playback-state"
))

# map NFC tags → albums
ALBUMS = {
    "album_01": "spotify:album:YOUR_ALBUM_ID"
}

@app.route("/play", methods=["POST"])
def play():
    data = request.json
    tag = data["tag"]

    uri = ALBUMS.get(tag)

    if uri:
        sp.start_playback(context_uri=uri)
        return "Playing", 200

    return "Unknown tag", 400

if __name__ == "__main__":
    app.run()