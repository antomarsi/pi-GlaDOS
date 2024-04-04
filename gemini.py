import google.generativeai as genai


class Gemini:

    def __init__(self, api_key: str) -> None:
        genai.configure(api_key=api_key)
        self.safety_settings = [
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
        self.context = "You are a sarcastic AI Virtual Assistant called glados, you mostly only anwser sarcastically, you should not break character in any moment, when asked to say something, you must say the text in character without mentioning that you are asked to say the text, you should not format any of your responses"
        self.history = []

    def load(self):
        self.model = genai.GenerativeModel('models/gemini-pro')
        self.chat = self.model.start_chat(history=[{
            "role": "user",
            "parts": [self.context]
        }, {
            "role": "model",
            "parts": "Okay",
        },])

    def send_message(self, text: str) -> str:
        print(text)
        response = self.chat.send_message(
            text, safety_settings=self.safety_settings)
        self.history = self.chat.history
        return response.text
