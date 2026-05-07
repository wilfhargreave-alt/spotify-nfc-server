import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ----------------------------
# LOAD ENV (IMPORTANT: FIRST)
# ----------------------------
load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

print("CLIENT ID LOADED:", CLIENT_ID)

# ----------------------------
# SPOTIFY AUTH
# ----------------------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state"
))

# ----------------------------
# NFC TAG → MUSIC MAP
# (PUT YOUR LINKS HERE)
# ----------------------------
MEDIA = {
    "album_01": "spotify:album:0f7R0jf0pcTb6K6IVVPcMD",
    "album_02": "spotify:album:6XvFfMcmZmAcntrLNWfUr5",
    "album_03": "spotify:album:2PmWuTXfKGX4Tx26VSdUQu",
    "album_04": "spotify:album:1y8VIK1Q5ajXcuMKmapNTE",

    "playlist_01": "spotify:playlist:5ImTk7pXbgVsL5gyEGooJD",
    "playlist_02": "spotify:playlist:3Dno4EcbWr8171XyDBD5Zr",
    "playlist_03": "spotify:playlist:6pjFYUvbS7UwFiHkGMAQeI",
    "playlist_04": "spotify:playlist:7LxtTl4VsVMSI5nTY4Zaax",
}

# ----------------------------
# FLASK APP
# ----------------------------
app = Flask(__name__)

@app.route("/play", methods=["POST"])
def play():
    data = request.json
    tag = data.get("tag")
    if tag not in MEDIA:
        return jsonify({"error": "Unknown tag"}), 400
    uri = MEDIA[tag]
    try:
        sp.start_playback(context_uri=uri)
        return jsonify({"status": "playing", "uri": uri})
    except Exception as e:
        print("SPOTIFY ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
# ----------------------------
# RUN SERVER
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)