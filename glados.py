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


class Glados:

    def __init__(self, model, gemini_api_key, spotify_creds) -> None:
        self.intent = IntentClassifier(model=model)
        self.gemini = Gemini(gemini_api_key)
        self.tts = TTSRunner(False, True)
        self.is_timeout = False
        self.sp = SpotifyClient(spotify_creds[0], spotify_creds[1])
        

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
        }

    async def take_command(self):

        # Feedback to user that GLaDOS is listening
        print('listening...')
        time.sleep(0.3)

        listener = sr.Recognizer()
        mic = sr.Microphone()

        # Record audio from the mic array
        with mic as source:

            # Collect ambient noise for filtering

            # listener.adjust_for_ambient_noise(source, duration=1.0)
            print("Speak... ")

            try:
                # Record
                voice = listener.listen(source, timeout=3)
                self.tts.play_audio("response_audio.wav")
                print("Got it...")

                # Speech to text
                command = listener.recognize_google(voice)
                command = command.lower()
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
                self.is_timeout = True
                print("Timeout; {0}".format(e))
            except Exception as e:
                print(e)
                result = self.gemini.send_message(
                    "Say that something went wrong")
                self.tts.speak(result)

    async def run(self):
        self.tts.play_audio("response_audio.wav")
        while (True):
            try:
                # Listen for command
                await self.take_command()
            except Exception as e:
                raise e