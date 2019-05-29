from pygame import mixer
from gtts import gTTS
from io import BytesIO
from time import sleep

mixer.init()

mp3_fp = BytesIO()
tts = gTTS('hello, this is a test. Oh, and i see you', 'en')
tts.write_to_fp(mp3_fp)
mp3_fp.seek(0)

mixer.music.load(mp3_fp)
mixer.music.play()
sleep(5)

