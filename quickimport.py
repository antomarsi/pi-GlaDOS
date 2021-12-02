import os
import json
from glob import glob
import re

folder = "data/audio"

data = {
    "magic-8-ball":[],
    "jokes": [],
    "clock": {
        "hour": [],
        "minute": [],
        "o": "clock/GLaDOS-o-clock.wav",
        "ding": {
            "off": "clock/GLaDOS_Announcer_ding_off.wav",
            "on": "clock/GLaDOS_Announcer_ding_on.wav"
            },
        "time-comment": {
            "general": [
                "clock/time-comment/GLaDOS-general-1-comment.wav",
                "clock/time-comment/GLaDOS-general-2-comment.wav",
                "clock/time-comment/GLaDOS-general-3-comment.wav",
                "clock/time-comment/GLaDOS-general-4-comment.wav",
            ],
            "hour": [
                "clock/time-comment/GLaDOS-hour-1-comment.wav",
                "clock/time-comment/GLaDOS-hour-6-comment.wav",
                "clock/time-comment/GLaDOS-hour-11-comment.wav",
                "clock/time-comment/GLaDOS-hour-22-comment.wav",
            ]
        }
        }
    }

files = [f for f in os.listdir(folder) if re.search(r'.+\D\.wav', f)]
for file in files:
    key = file.replace(".wav", "").replace("GLaDOS-", "")
    data[key] = file

files = [f for f in os.listdir(folder) if re.search(r'.+\d+\.wav', f)]
for file in files:
    key = file.replace(".wav", "").replace("GLaDOS-", "")
    key = re.sub('-\d+', '', key)
    if (data.get(key)):
        data[key].append(file)
    else:
        data[key] = [file]

files = os.listdir(os.path.join(folder, "magic-8-ball"))
for file in files:
    data["magic-8-ball"].append("magic-8-ball/"+file)

files = os.listdir(os.path.join(folder, "jokes"))
for file in files:
    data["jokes"].append("jokes/"+file)

files = os.listdir(os.path.join(folder, "clock", "hour"))
for file in files:
    data["clock"]["hour"].append("clock/hour/"+file)

files = os.listdir(os.path.join(folder, "clock", "minute"))
for file in files:
    data["clock"]["minute"].append("clock/minute/"+file)

export = "data/default.json"

with open(export, "w") as f:
    f.write(json.dumps(data, indent=4))