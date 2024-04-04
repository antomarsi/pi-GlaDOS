from gladosTTS import TTSRunner
import time
import speech_recognition as sr
from intent import IntentClassifier
from gemini import Gemini
from actions.out_of_scope_action import OutOfScopeAction
from actions.music_action import MusicAction
from actions.give_time_action import GiveTimeAction
import threading
from spotify import SpotifyClient
import traceback
from exceptions.spotify_exceptions import SpotifyDeviceNotFoundError
from actions.weather_action import WeatherAction

class Glados:

    def __init__(self, model, gemini_api_key, spotify_creds, openweather_apikey, trigger_word = None) -> None:
        self.intent = IntentClassifier(model=model)
        self.gemini = Gemini(gemini_api_key)
        self.tts = TTSRunner(False, True)
        self.is_timeout = False
        self.sp = SpotifyClient(spotify_creds[0], spotify_creds[1])
        self.trigger_word = trigger_word
        self.openweather_apikey = openweather_apikey
        

    def load(self):
        threads = []
        load_actions = [
            self.intent.load,
            self.gemini.load,
            self.tts.load
        ]
        for action in load_actions:
            x = threading.Thread(target=action, args=())
            threads.append(x)
            x.start()

        for t in threads:
            t.join()

        music_action = MusicAction(self.gemini, self.tts, self.sp)

        self.scopes = {
            "out_of_scope": {"action": OutOfScopeAction(self.gemini, self.tts)},
            "play_music": {"action": music_action, "command": "play_music"},
            "next_music": {"action": music_action, "command": "next_music"},
            "stop_music": {"action": music_action, "command": "stop_music"},
            "resume_music": {"action": music_action, "command": "resume_music"},
            "give_time": {"action": GiveTimeAction(self.gemini, self.tts)},
            "give_weather": {"action": WeatherAction(self.gemini, self.tts, self.openweather_apikey)}
        }

    async def take_command(self):

        listener = sr.Recognizer()

        # Record audio from the mic array
        with sr.Microphone() as source:

            # Collect ambient noise for filtering

            listener.adjust_for_ambient_noise(source, duration=0.2)

            try:
                # Record
                voice = listener.listen(source)

                # Speech to text
                command = listener.recognize_google(voice)
                command = command.lower()

                if self.trigger_word is None or any(word in command for word in self.trigger_word):
                    self.tts.play_audio("response_audio.wav")
                    while True:
                        print('listening...')
                        voice = listener.listen(source, timeout=3)
                        command = listener.recognize_google(voice)
                        command = command.lower()
                        if command is None:
                            return

                        response = await self.intent.find_intent(command)

                        if (response["intent"]):
                            if response["intent"] in self.scopes:
                                scope = self.scopes[response["intent"]]
                                if "command" in scope:
                                    command = getattr(scope["action"], scope["command"])
                                    command(response)
                                else:
                                    scope["action"].run(response)
                            else:
                                raise Exception("no scope found")

            # No speech was heard
            except sr.WaitTimeoutError as e:
                print("Timeout; {0}".format(e))
                return
            except sr.exceptions.UnknownValueError:
                print("speech_recognition: UnknownValueError")
            except SpotifyDeviceNotFoundError as e:
                print(e)
                result = self.gemini.send_message(
                    "Say that i don't have Spotify open and i need to open Spotify if i want to continue, keep the response small")
                self.tts.speak(result)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                result = self.gemini.send_message(
                    "Say that something went wrong, and keep the response very small")
                self.tts.speak(result)

    async def run(self):
        self.tts.play_audio("response_audio.wav")
        while (True):
            try:
                # Listen for command
                await self.take_command()
            except Exception as e:
                raise e