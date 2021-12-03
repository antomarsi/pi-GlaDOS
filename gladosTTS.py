import os
import simpleaudio as sa
import requests
import json
import uuid
import random
import time
class GladosTTS():
    def __init__(self) -> None:
        self.data = os.getenv('TTS_SAMPLE_FOLDER', "data")


        self.audio_path = os.path.join(self.data, "audios")
        if not os.path.exists(self.audio_path):
            os.makedirs(self.audio_path)
        self.phrase_file = os.path.join(self.data, "voices.json")
        self.audio_dict = {}

        if (not os.path.isfile(self.phrase_file)):
            self.save_database()
        else:
            with open(self.phrase_file) as f:
                self.audio_dict = json.load(f)

        self.defaul_audio_path = os.path.join(self.data, "default")
        with open(os.path.join(self.data, "default.json")) as f:
            self.default_audio_dict = json.load(f)

    def save_database(self):
        with open(self.phrase_file, 'w') as outfile:
            json.dump(self.audio_dict, outfile, indent=4)
        

    def playFile(self, filename):
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    # Turns units etc into speakable text

    def cleanTTSLine(self, line):
        line = line.replace("°C", "degrees celcius")
        line = line.replace("°", "degrees")
        line = line.replace("hPa", "hectopascals")
        line = line.replace("% (RH)", "percent")
        line = line.replace("g/m³", "grams per cubic meter")
        line = line.replace("sauna", "incinerator")
        line = line.lower()

        return line

    # Cleans filename for the sample

    def cleanTTSFile(self, line):

        filename = self.cleanTTSLine(line).replace(" ", "-")
        filename = filename.replace("!", "")
        filename = filename.replace("°c", "degrees celcius")
        filename = filename.replace(",", "-")

        return filename

    # Return the path of a TTS sample if found in the library

    def checkTTSLib(self, line):
        filename = self.audio_dict.get(self.cleanTTSFile(line))
        if (filename is not None):
            return os.path.join(self.audio_path, filename)
        return False

    # Get GLaDOS TTS Sample over the online API

    def fetchTTSSample(self, line, wait=True):
        filename = uuid.uuid4().hex + ".wav"
        data = {
            'text': line
        }
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}

        max_retry = 30
        retries = 0
        success = False
        while retries < max_retry and success is False:
            try:
                response = requests.get('https://glados.c-net.org/generate', params=data, headers=headers)
                success = True
            except Exception as e:
                time.sleep(0.5)
                retries += 1
        
        file_path = os.path.join(self.audio_path, filename)
        key = self.cleanTTSFile(line)

        self.audio_dict[key] = filename

        with open(file_path, 'wb') as f:
            f.write(response.content)
        self.save_database()
        return  os.path.join(self.audio_path, filename)

    # Speak out the line
    def speak(self, line):

        # Limitation of the TTS API
        if(len(line) < 255):

            file = self.checkTTSLib(line)

            # Check if file exists
            if file:
                self.playFile(file)
                print(line)

            # Else generate file
            else:
                print("File not exist, generating...")

                # Play "hold on"
                self.playRandom("wait")

                # Try to get wave-file from https://glados.c-net.org/
                # Save line to TTS-folder
                file_line = self.fetchTTSSample(line)
                if(file_line):
                    self.playFile(file_line)

    def playRandom(self, keyword):
        self.playFile(os.path.join(self.defaul_audio_path, random.choice(self.default_audio_dict[keyword])))
    
    def playDefaultRandom(self, keyword):
        keywords = keyword.split("_")
        if len(keywords) == 1:
            file = self.default_audio_dict[keyword]
        else:
            file = self.default_audio_dict
            for key in keywords:
                file = file[key]
        self.playFile(os.path.join(self.defaul_audio_path, random.choice(file)))


    def playDefault(self, keyword, index = None):
        keywords = keyword.split("_")
        if len(keywords) == 1:
            file = self.default_audio_dict[keyword]
        else:
            file = self.default_audio_dict
            for key in keywords:
                file = file[key]
        if (index is not None):
                file = file[index]
        self.playFile(os.path.join(self.defaul_audio_path, file))

    def playTime(self, hour, minute):
        
        print(hour+":"+minute)
        self.playDefault("clock_hour_"+hour)
        self.playDefault("clock_minute_"+minute)
        r = random.randint(1, 10)

        if (r <= 4):
            hour = hour.lstrip('0')
            if self.default_audio_dict["clock"]["time-comment"]["hour"].get(hour) is not None:
                self.playDefault("clock_time-comment_hour_"+hour)
            else:
                self.playDefaultRandom("clock_time-comment_general")
