from gemini import Gemini
from gladosTTS import TTSRunner
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify import SpotifyClient


class MusicAction():

    def __init__(self, gemini: Gemini, tts: TTSRunner, spotify_client: SpotifyClient) -> None:
        self.gemini = gemini
        self.tts = tts
        self.sp = spotify_client

    def play_music(self, rasa_response):
        self.sp.update_device()
        band_name = None
        music_name = None
        for entity in rasa_response["entities"]:
            if entity["entity"] == "band_name":
                band_name = entity["value"]
            elif entity["entity"] == "music_name":
                music_name = entity["value"]
        if band_name is None or music_name is None:
            raise Exception("skill issue")
        text = self.gemini.send_message(
            f"say that you gonna play the music {music_name} with the band {band_name}")
        self.tts.speak(text)
        self.sp.play_music(music_name, band_name)
    
    def stop_music(self, _):
        self.sp.update_device()
        text = self.gemini.send_message(
            f"say that you gonna stop the music")
        self.tts.speak(text)
        self.sp.stop_music()

    def next_music(self, _):
        self.sp.update_device()
        text = self.gemini.send_message(
            f"say that you gonna play the next music")
        self.tts.speak(text)
        self.sp.next_music()
        
    def resume_music(self, _):
        self.sp.update_device()
        text = self.gemini.send_message(
            f"say that you gonna resume playing the music, don't mention anything about the music name or band")
        self.tts.speak(text)
        self.sp.resume_music()
