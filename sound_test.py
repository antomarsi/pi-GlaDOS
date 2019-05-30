import speake3
from random import randint

engine = speake3.Speake()
text = "Hello, and, again, welcome to the Aperture Science Computer-aided Enrichment Center"
text = text.split()
words = []
for word in text:
    words.append("<prosody pitch=\"%d\">%s</prosody>" % (randint(0, 100)-50, word))
text = " ".join(words)
print (text)

engine = speake3.Speake()  # Initialize the speake engine
engine.set('voice', 'en+f3')
engine.set('speed', '180')
engine.set('pitch', '60')
engine.set('markup')
engine.say(text)  # String to be spoken
engine.talkback()
