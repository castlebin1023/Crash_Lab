import speech_recognition as sr
from gtts import gTTS
import pygame

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>STT MODEL<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def find_mic(): # Microphone(device_index=##)
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
        
def adjust_noise(index,adj_time):
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index = index)
    with mic as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source,duration=adj_time)  #Noise correction for adj_time
        print(f"Adjusted energy threshold: {recognizer.energy_threshold}")
        print("Please enter your voice for check noise. . .")
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing. . .")
        text = recognizer.recognize_google(audio, language="ko-KR") #Korean recognition, !!50 TIME A DAY!!
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Voice not recognized.")
        return None
    except sr.RequestError as e:
        print(f"Can't access Google API; {e}")
        return None 


def google_free(index):
    # Voice recognition settings on the microphone
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index = index)

    # Voice capture by mic
    with mic as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)  #Noise correction for 1 Sec
        print("Please enter your voice. . .")
        audio = recognizer.listen(source)

    # Attempt to convert voice to text
    try:
        print("Recognizing. . .")
        text = recognizer.recognize_google(audio, language="ko-KR") #Korean recognition, !!50 TIME A DAY!!
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Voice not recognized.")
        return None
    except sr.RequestError as e:
        print(f"Can't access Google API; {e}")
        return None 
    
def google_cloudspeech(index):
    # Voice recognition settings on the microphone
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=index)

    # Voice capture by mic
    with mic as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)  #Noise correction for 1 Sec
        print("Please enter your voice. . .")
        audio = recognizer.listen(source)
    
    #Attempt to convert voice to text
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
    try:
        print("Recognizing. . .")
        text = recognizer.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS,language="ko-KR")
        print("You said",text)
        return text
    except sr.UnknownValueError:
        print("Voice not recognized.")
        return None
    except sr.RequestError as e:
        print(f"Can't access Google API; {e}")
        return None

class BackgroundSpeechRecognizer:
    def __init__(self, index):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=index)
        self.stop_listening = None

    def _callback(self, recognizer, audio):
        """Background thread callback to process audio with Google Speech Recognition."""
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio,language="ko-KR")
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Voice not recognized.")
            return None
        except sr.RequestError as e:
            print(f"Can't access Google API; {e}")
            return None

    def start_listening(self):
        """Start listening in the background."""
        with self.microphone as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source)
        
        print("Please enter your voice...")
        # Start background listening *outside* the with-block for source
        self.stop_listening = self.recognizer.listen_in_background(self.microphone, self._callback)

    def stop_listening(self, wait_for_stop=False):
        """Stop listening in the background."""
        if self.stop_listening:
            self.stop_listening(wait_for_stop=wait_for_stop)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>TTS MODEL<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def speak(text,use_lang):
    tts = gTTS(text,lang=use_lang)
    tts.save("/home/castlebin/code_ws/Crash_Lab/mp3_file/output.mps")
    pygame.mixer.init()
    pygame.mixer.music.load("/home/castlebin/code_ws/Crash_Lab/mp3_file/output.mps")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue
    return None 
