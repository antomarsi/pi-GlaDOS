from gemini import Gemini
from gladosTTS import TTSRunner

class OutOfScopeAction():

    def __init__(self, gemini: Gemini, tts: TTSRunner) -> None:
        self.gemini = gemini
        self.tts = tts

    def run(self, rasa_response):
        text = self.gemini.send_message(rasa_response["text"])
        self.tts.speak(text)
        