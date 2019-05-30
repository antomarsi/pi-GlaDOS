import speake3
from random import randint

text = '<prosody pitch=\"-2\">Hello,</prosody> <prosody pitch=\"+31%\">and,</prosody> <prosody pitch=\"-18\">again,</prosody> <prosody pitch=\"-44\">welcome</prosody> <prosody pitch=\"-15\">to</prosody> <prosody pitch=\"-43\">the</prosody> <emphasis level=\"strong\"><prosody pitch=\"-18\">Aperture</prosody> <prosody pitch=\"+23\">Science</prosody> <prosody pitch=\"+39\">Computer-aided</prosody> <prosody pitch=\"+41\">Enrichment</prosody> <prosody pitch=\"-10\">Center</prosody></emphasis>'


engine = speake3.Speake()  # Initialize the speake engine
engine.set('voice', 'en+f3')
engine.set('speed', '180')
engine.set('markup')
engine.say(text)  # String to be spoken
engine.talkback()
# espeak -m -ven+f2 -s 180 -p 60 "<speak><s><prosody rate=\"x-slow\">Oh</prosody> <break time=\"1s\"/>, <prosody rate=\"slow\">i</prosody> <prosody rate=\"slow\">see</prosody> <prosody rate=\"slow\">you</prosody></s></speak>"
#   for a in `cat`; do
#     V=$(((($RANDOM) % 100) - 50))
#     echo -n "<prosody pitch=\"+$V\">$a</prosody> " |
#       sed 's/+-/-/' 
#   done |
#   espeak -ven+f3 -m -p 20 -s 180