from gemini import Gemini
from gladosTTS import TTSRunner
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class PlayMusicAction():

    def __init__(self, gemini: Gemini, tts: TTSRunner) -> None:
        self.gemini = gemini
        self.tts = tts
        auth = SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            scope=" ".join([
                "user-read-playback-state",
                "user-modify-playback-state",
                "streaming",
                "app-remote-control",
                "playlist-read-private",
                "playlist-modify-public"
            ]),
            redirect_uri="http://localhost:8080/callback",
        )
        self.sp = spotipy.Spotify(auth_manager=auth)
        self.selected_device = self.last_device_id()

    def last_device_id(self):
        devices = self.sp.devices()
        current_device = None
        for device in devices["devices"]:
            if device["is_active"] is True:
                current_device = device["id"]
                break
        if current_device is None:
            current_device = devices["devices"][0]["id"]
        return current_device

    def run(self, rasa_response):
        band_name = None
        music_name = None
        for entity in rasa_response["entities"]:
            if entity["entity"] == "band_name":
                band_name = entity["value"]
            elif entity["entity"] == "music_name":
                music_name = entity["value"]
        if band_name is None or music_name is None:
            raise Exception("skill issue")
        result = self.search_music(music_name, band_name)
        text = self.gemini.send_message(
            f"say that you gonna play the music {music_name} with the band {band_name}")
        self.tts.speak(text)
        self.sp.start_playback(device_id=self.selected_device, uris=[result])

    def search_music(self, music_name, band_name):
        new_query = f"track:{music_name} artist:{band_name}"
        results = self.sp.search(new_query, type='track', limit=10)
        return results['tracks']['items'][0]["uri"]
