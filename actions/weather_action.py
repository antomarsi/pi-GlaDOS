from gemini import Gemini
from gladosTTS import TTSRunner
import geocoder
import requests

class WeatherAction():

    def __init__(self, gemini: Gemini, tts: TTSRunner, openweather_apikey:str) -> None:
        self.gemini = gemini
        self.tts = tts
        self.api_key = openweather_apikey
    
    def get_weather(self, lat, lon):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        return response.json()

    def run(self, rasa_response):
        localization = geocoder.ip("me")
        [lat, lng] = localization.latlng
        response = self.get_weather(lat, lng)

        text = self.gemini.send_message(
            f"""using the following weather data:
                City: {response["name"]}
                Temperature: {response["main"]["temp"]}
                Weather: {response["weather"][0]["main"]}
                
                Answer the following question, don't forget to always say if it's raining and the current temperature:
                {rasa_response["text"]}
                """)
        self.tts.speak(text)
        