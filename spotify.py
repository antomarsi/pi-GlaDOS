import json
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from exceptions.spotify_exceptions import SpotifyDeviceNotFoundError


class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str) -> None:
        auth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
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

    def update_device(self):
        devices = self.sp.devices()
        current_device = None
        for device in devices["devices"]:
            if device["is_active"] is True:
                current_device = device["id"]
                break
        if current_device is None and len(devices["devices"]):
            current_device = devices["devices"][0]["id"]
        if current_device is None:
            raise SpotifyDeviceNotFoundError("Spotify device not found")
        self.selected_device = current_device

    def search_music(self, music_name, band_name):
        new_query = f"track:{music_name} artist:{band_name}"
        results = self.sp.search(new_query, type='track', limit=10)
        return results['tracks']['items'][0]["uri"]

    def play_music(self, music, band):
        result = self.search_music(music, band)
        self.sp.start_playback(device_id=self.selected_device, uris=[result])

    def next_music(self):
        self.sp.next_track(device_id=self.selected_device)
    
    def stop_music(self):
        self.sp.pause_playback(device_id=self.selected_device)
    
    def resume_music(self):
        self.sp.start_playback(device_id=self.selected_device)