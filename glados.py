from gladosTTS import GladosTTS
import speech_recognition as sr
from pocketsphinx import LiveSpeech
import time
import os
import psutil
import sys
import datetime as dt

class Glados:
    def __init__(self) -> None:
        self.tts = GladosTTS()

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

            speech = LiveSpeech(keyphrase=os.getenv('TRIGGERWORD', "hey alexa"), lm=False, kws_threshold=1e-20)
            for phrase in speech:
                try:
                    # Listen for command
                    command = self.take_command()
                    # Execute command
                    self.process_command(command)
                except Exception as e:
                    # Something failed
                    print(e)
            print("finished")

    def take_command(self):

        # Feedback to user that GLaDOS is listening
        print('listening...')
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

                # Save input as file as later training data
                #timestamp = str(int(dt.datetime.now().timestamp()))
                # with open("/home/nerdaxic/GLaDOS/collectedSpeech/" + timestamp+" "+command+".wav", "wb") as f:
                #	f.write(voice.get_wav_data(convert_rate=16000))

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

        if 'cancel' in command:
            self.tts.playRandom("cancel")
            failList = open("cancelledActivations.log", "a")
            failList.write('\n'+str(os.getenv('TRIGGERWORD'))+" "+str(os.getenv('TRIGGERWORD_TRESHOLD')));
            failList.close()

        elif 'timer' in command:
            #startTimer(command)
            self.tts.speak("Sure.")
        elif 'time' in command:
            #readTime()
            pass

        elif ('should my ' in command or 
            'should I ' in command or
            'should the ' in command or
            'shoot the ' in command):
            self.tts.playRandom("magic-8-ball")

        elif 'joke' in command:
            self.tts.playRandom("jokes")

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

        else:
            print("Command not recognized")
            self.tts.playRandom("rec-fail")

            failList = open("failedCommands.log", "a")
            failList.write('\n'+command);
            failList.close()

        print("Waiting for trigger...")