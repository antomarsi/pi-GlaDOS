import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')

print(voices)

engine.say("I will speak this text")
engine.runAndWait()