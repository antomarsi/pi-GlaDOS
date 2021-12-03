from random import random
from gladosTTS import GladosTTS
import speech_recognition as sr
from pocketsphinx import LiveSpeech, get_model_path
import time
import os
import psutil
import sys
import datetime as dt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
from flask import Flask

model_path = get_model_path()
CACHE = '.spotipyoauthcache'
class Glados:
    def __init__(self) -> None:
        self.app = Flask("Glados")
        self.tts = GladosTTS()
        scope = [
            "user-read-playback-state",
            "user-modify-playback-state",
            "streaming",
            "app-remote-control",
            "playlist-read-private",
            "playlist-modify-public"
        ]
        token = spotipy.util.prompt_for_user_token(
            os.getenv("SPOTIPY_USERNAME"),
            client_id=os.getenv("SPOTIFY_ID"),
            client_secret=os.getenv("SPOTIFY_SECRET"),
            scope=" ".join(scope),
            redirect_uri="http://localhost:8080/callback",
            cache_path=CACHE
        )
        self.sp = spotipy.Spotify(auth=token)
        self.selected_device = self.last_device_id()

    def restart_program():
        try:
            p = psutil.Process(os.getpid())
            for handler in p.get_open_files() + p.connections():
                os.close(handler.fd)
        except Exception as e:
            print(e)

        python = sys.executable
        os.execl(python, python, *sys.argv)

    def run(self):
            if (os.getenv("SKIP_INTRO", "False") == "False"):
                self.tts.speak("oh, its you")
                time.sleep(0.25)
                self.tts.speak("it's been a long time")
                time.sleep(1.5)
                self.tts.speak("how have you been")
            if (os.getenv("SKIP_TRIGGER", "False") == "False"):
                speech = LiveSpeech(
                    keyphrase=os.getenv('TRIGGERWORD', "hey alexa"),
                    kws_threshold=1e-20,
                    lm=False
                )
                for phrase in speech:
                    try:
                        # Listen for command
                        command = self.take_command()
                        # Execute command
                        self.process_command(command)
                    except Exception as e:
                        # Something failed
                        print(e)
            else:
                while(True):
                    try:
                            # Listen for command
                        command = self.take_command()
                        # Execute command
                        self.process_command(command)
                        time.sleep(2)
                    except Exception as e:
                        print(e)
            print("finished")

    def last_device_id(self):
        devices = self.sp.devices()
        current_device = None
        for device in devices["devices"]:
            if device["is_active"] is True:
                current_device = device["id"]
                break
        if current_device is None:
            current_device = devices["devices"][0]["id"]
        return current_device



    def take_command(self):
 
        # Feedback to user that GLaDOS is listening
        print('listening...')
        time.sleep(0.3)
        self.tts.playRandom("detect-pass")

        listener = sr.Recognizer()
        mic = sr.Microphone()

        # Record audio from the mic array
        with mic as source:

            # Collect ambient noise for filtering

            #listener.adjust_for_ambient_noise(source, duration=1.0)
            print("Speak... ")

            try:
                # Record
                voice = listener.listen(source, timeout=3)

                print("Got it...")

                # Speech to text
                command = listener.recognize_google(voice)
                command = command.lower()

                print("I heard: "+command)

                # Remove possible trigger word from input
                if os.getenv('TRIGGERWORD') in command:
                    command = command.replace(os.getenv('TRIGGERWORD'), '')

                return command

            # No speech was heard
            except sr.WaitTimeoutError as e:
                print("Timeout; {0}".format(e))

            # STT API failed to process audio
            except sr.UnknownValueError:
                print("Google Speech Recognition could not parse audio")
                # self.tts.speak("My speech recognition core could not understand audio")

                #timestamp = str(int(dt.datetime.now().timestamp()))
                # with open("/home/nerdaxic/GLaDOS/collectedSpeech/" + timestamp+" fail.wav", "wb") as f:
                #	f.write(voice.get_wav_data(convert_rate=8000))

            # Connection to STT API failed
            except sr.RequestError as e:
                print(
                    "Could not request results from Google Speech Recognition service; {0}".format(e))

        

    def process_command(self, command):
        if command is None:
            return

        if 'cancel' in command:
            self.tts.playRandom("cancel")
            failList = open("cancelledActivations.log", "a")
            failList.write('\n'+str(os.getenv('TRIGGERWORD'))+" "+str(os.getenv('TRIGGERWORD_TRESHOLD')));
            failList.close()

        elif 'timer' in command:
            #startTimer(command)
            self.tts.speak("Sure.")

        elif ('should my ' in command or 
            'should I ' in command or
            'should the ' in command or
            'shoot the ' in command):
            self.tts.playRandom("magic-8-ball")

        elif 'joke' in command:
            self.tts.playRandom("jokes")

        elif "time" in command:
            timer=dt.datetime.now()
            hour = timer.strftime('%H')
            minute = timer.strftime('%M')
            self.tts.playTime(hour, minute)

        elif 'who are' in command:
            self.tts.playDefault("intro", 0)

        elif 'can you do' in command:
            self.tts.playDefault("intro", 1)

        ##### PLEASANTRIES ###########################
        elif 'how are you' in command:
            self.tts.speak("I'm still a bit mad about being unplugged not a long time ago.")
            self.tts.speak("you murderer")

        elif 'can you hear me' in command:
            self.tts.speak("Yes, I can hear you loud and clear")

        elif 'good morning' in command:
            if 6 <= dt.datetime.now().hour <= 12:
                self.tts.speak("great, I have to spend another day with you")
            elif 0 <= dt.datetime.now().hour <= 4:
                self.tts.speak("do you even know, what the word morning means")
            else:
                self.tts.speak("well it ain't exactly morning now is it")

        # Used to calibrate ALSAMIX EQ 
        elif 'play pink noise' in command:
            self.tts.speak("I shall sing you the song of my people.")
            self.tts.playDefault("pinknoise")

        elif 'restart' in command or 'reload' in command:
            self.tts.speak("Cake and grief counseling will be available at the conclusion of the test.")
            self.restart_program()
        
        # Spotify
        elif "next song" in command:
            self.tts.speak("Playing next song")
            self.sp.next_track()

        elif "previous  song" in command:
            self.tts.speak("Playing previous song")
            self.sp.previous_track()

        elif "pause" in command:
            self.tts.speak("Pausing")
            self.sp.pause_playback()
            
        # Play Track
        elif "play" in command and "album" in command:
            query = command.replace('play', '')
            query = query.replace('please', '')
            query = query.replace('album', '')
            query = query.replace('  ', '')
            try:
                results = self.sp.search(query, type='album', limit=1)
                for i, t in enumerate(results['albums']['items']):
                    uri = t['uri']
                self.tts.playDefault('clock_ding_on')
                current = self.sp.start_playback(device_id=self.selected_device, context_uri=uri)
                if len(uri) == 0:
                    self.tts.speak("No album found, your memory is failing you")
            except:
                self.tts.speak("No album found, your memory is failing you")
                print('No album found')
        elif "play" in command and "playlist" in command:
                query = command.replace('playlist', '')
                query = query.replace('please', '')
                query = query.replace('play', '')
                query = query.replace('  ', '')
                try:
                    results = self.sp.search(query, type='playlist', limit=1)
                    for i, t in enumerate(results['playlists']['items']):
                        uri = t['uri']
                    self.tts.playDefault('clock_ding_on')
                    current = self.sp.start_playback(device_id=self.selected_device, context_uri=uri)
                    if len(uri) == 0:
                        self.tts.speak("No playlist found")
                except:
                    self.tts.speak("No playlist found")
                    print('No playlist found')

        elif "play" in command:
            print("playing music")
            query = command.replace('play', '')
            query = query.replace('please', '')
            query = query.replace('  ', '')

            try:
                uris = []
                splited = query.split(" from ")
                results = None
                name = splited[0].strip()
                artist = splited[1].strip()
                if len(splited) > 1:
                    new_query = "track:"+name+" artist:" +artist
                    print("searching using artist and track")
                    print(new_query)
                    results = self.sp.search(new_query, type='track', limit=10)
                    print(results)
                if results is None:
                    results = self.sp.search(query, type='track', limit=10)
                for i, t in enumerate(results['tracks']['items']):
                    uri = t['uri']
                    uris.append(uri)
                    break
                self.tts.playDefault('clock_ding_on')
                print(uris)
                self.sp.start_playback(device_id=self.selected_device, uris=uris)
                if len(uris) == 0:
                    self.tts.speak('No track found, maybe you should study more about culture')
            except Exception as e:
                print(e)
                self.tts.speak('No track found, maybe you should study more about culture')
                print('No track found')
        else:
            print("Command not recognized")
            self.tts.playRandom("rec-fail")

            failList = open("failedCommands.log", "a")
            failList.write('\n'+command);
            failList.close()
        print("Waiting for trigger...")