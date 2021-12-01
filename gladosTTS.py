import os
import subprocess
import pyaudio
import wave
from random import randint
import _thread as thread
from threading import Timer
import sys
from dotenv import load_dotenv
import requests
import time
import json
import uuid

class GladosTTS():
    def __init__(self) -> None:
        load_dotenv()
        self.synthFolder = os.getenv('TTS_SAMPLE_FOLDER', "data")
        if not os.path.exists(self.synthFolder):
            os.makedirs(self.synthFolder)
        self.audio_path = os.path.join(self.synthFolder, "audios")
        if not os.path.exists(self.audio_path):
            os.makedirs(self.audio_path)
        self.phrase_file = os.path.join(self.synthFolder, "voices.json")
        self.audio_dict = {}
        if (not os.path.isfile(self.phrase_file)) {
            self.save_database()
        }

    def save_database(self):
        with open(self.phrase_file, 'w') as outfile:
            json.dump(self.audio_dict, outfile)
        

    def playFile(self, filename):

        # Defines a chunk size of 1024 samples per data frame.
        chunk = 1024

        # Open sound file  in read binary form.
        file = wave.open(filename, 'rb')

        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Creates a Stream to which the wav file is written to.
        # Setting output to "True" makes the sound be "played" rather than recorded
        stream = p.open(format=p.get_format_from_width(file.getsampwidth()),
                        channels=file.getnchannels(),
                        rate=file.getframerate(),
                        output=True,
                        output_device_index=int(os.getenv('SOUND_CARD_ID')))

        # Read data in chunks
        data = file.readframes(chunk)

        # Play the sound by writing the audio data to the stream

        while True:
            data = file.readframes(chunk)
            if not data:
                break
            stream.write(data)  # to be played

        time.sleep(0.1)

        # Stop, Close and terminate the stream
        stream.stop_stream()
        stream.close()
        # p.terminate() for some reason uncommenting this crashes notify api

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

        filename = "GLaDOS-tts-"+self.cleanTTSLine(line).replace(" ", "-")
        filename = filename.replace("!", "")
        filename = filename.replace("°c", "degrees celcius")
        filename = filename.replace(",", "")+".wav"

        return filename

    # Return the path of a TTS sample if found in the library

    def checkTTSLib(self, line):
        line = self.cleanTTSLine(line)
        if line in self.audio_dict:
            return self.audio_dict.get(line)
        return False

    # Get GLaDOS TTS Sample over the online API

    def fetchTTSSample(self, line, wait=True):
        filename = uuid.uuid4()
        data = {
            'text': line
        }
        response = requests.get('https://glados.c-net.org/generate', data=data)
        
        response.raise_for_status()
        
        file_path = os.path.join(self.audio_path, filename + ".wav")
        self.audio_dict[filename] = line
        with open(file_path, 'wb') as f:
            f.write(response.content)
        self.save_database()
        return 

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
                # TODO set the default path for default audios
                self.playFile(
                              '/audio/GLaDOS-wait-'+str(randint(1, 6))+'.wav')

                # Try to get wave-file from https://glados.c-net.org/
                # Save line to TTS-folder
                if(self.fetchTTSSample(line)):
                    self.playFile(self.synthFolder+self.cleanTTSFile(line))
