from pocketsphinx import LiveSpeech, get_model_path
from dotenv import load_dotenv
import speech_recognition as sr
import os


load_dotenv()

model_path = get_model_path()


def take_command():

    # Feedback to user that GLaDOS is listening
    print('listening...')
    #playFile(os.path.dirname(os.path.abspath(__file__))+'/audio/GLaDOS-detect-pass-'+str(randint(1, 20))+'.wav')

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
            # speak("My speech recognition core could not understand audio")

            #timestamp = str(int(dt.datetime.now().timestamp()))
            # with open("/home/nerdaxic/GLaDOS/collectedSpeech/" + timestamp+" fail.wav", "wb") as f:
            #	f.write(voice.get_wav_data(convert_rate=8000))

        # Connection to STT API failed
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

speech = LiveSpeech(keyphrase=os.getenv('TRIGGERWORD', "hey alexa"), lm=False, kws_threshold=1e-20)
for phrase in speech:
    try:
        # Listen for command
        command = take_command()
        # Execute command
        print(command)
    except Exception as e:
        # Something failed
        print(e)
