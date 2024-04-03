from gemini import Gemini
from gladosTTS import TTSRunner
import datetime as dt

class GiveTimeAction():

    def __init__(self, gemini: Gemini, tts: TTSRunner) -> None:
        self.gemini = gemini
        self.tts = tts

    def run(self, rasa_response):
        now = dt.datetime.now().strftime("%H:%M")
        text = self.gemini.send_message(
            f"say that the time is {now}")
        self.tts.speak(text)
        