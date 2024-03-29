import google.generativeai as genai
from tts.gladosTTS import TTSRunner
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

safety_settings = [
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

context = '''You are a sarcastic AI Virtual Assistant called glados, you mostly only anwser sarcastically, you should not break character in any moment, the response should always be in a JSON format without breaking the JSON format or return a JSON inside a JSON, nothing before and nothing after, you need to return in the following json format:
{
    "message": "",
    "command": "",
    "command_values": ""
}

the "message" attribute is the message returned by the virtual assistant to the user.
the "command" attribute is the key word if the user ask for a action, if the user doesn't ask for a action, return "command" as a empty string, the following list show the available keywords and the description:
play_music: the user asked to play a music or song
clock: the user asked the time

the "command_values" attribute is the values related to the action, if there's no action or values related, should return "command_values" as a empty string, the following list show the values that you should return for each action:
play_music: you need to return the name of the song and the band
'''

model = genai.GenerativeModel('models/gemini-pro')

history = []

if __name__ == "__main__":
    glados = TTSRunner(False, True)
    while True:
        text = input("Input: ")
        if len(text) > 0:
            try:
                if len(history) == 0:
                    history.append({
                        "role": "user",
                        "parts": [context, text]
                    })
                else:
                    history.append({
                        "role": "user",
                        "parts": [text]
                    })
                response = model.generate_content(history, safety_settings=safety_settings)
                print(response.text)
                res = json.loads(response.text)
                history.append({
                    "role": "model",
                    "parts": [response.text]
                })
                glados.speak(res["message"], True)
                print(res)
                if res["command"]:
                    if res["command"] == "clock":
                        glados.speak("The time is {}".format(time.strftime("%H %M")), True)
            except Exception as e:
                print(e)
                #print(response.prompt_feedback)