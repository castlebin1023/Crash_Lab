#>>>>>>>>>>>>>>>>>>>>>>>mic tuning<<<<<<<<<<<<<<<<<<<<<<<<<#
import speech_recognition as sr 
import pygame
import time
#>>>>>>>>>>>>>>>>>>>STT MODEL<<<<<<<<<<<<<<<<<<<<<<<<<<<
import sounddevice as sd
import wave
from usb_4_mic_array.tuning import Tuning
from pixel_ring.usb_pixel_ring_v2 import PixelRing
import atexit
#>>>>>>>>>>>>>>>>>>>>>>>TTS MODEL<<<<<<<<<<<<<<<<<<<<<<<<<#
from gtts import gTTS
#>>>>>>>>>>>>>>>>>>>>>>>gpt<<<<<<<<<<<<<<<<<<<<<<<<<#
import openai
from openai import OpenAI


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
        
class BackgroundSpeechRecognizer:
    def __init__(self, index, keywords):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=index)
        self.keywords = keywords if keywords else []
        self.stop_listening = None
        self.trigger = False
        self.recognized_text = None
        
        #set parm
        self.recognizer.non_speaking_duration = 0.3
        self.recognizer.pause_threshold = 0.5 

    def _callback(self, recognizer, audio):
        """Background thread callback to process audio with Google Speech Recognition."""
        try:
            print("Recognizing...")
            self.recognized_text = recognizer.recognize_google(audio,language="ko-KR") 
            # text = recognizer.recognize_google_cloud(
            # audio,
            # language="ko-KR" 
            # )
            print("You said:", self.recognized_text)
            for keyword in self.keywords:
                if keyword in self.recognized_text:
                    print(f"Keyword '{keyword}' detected!")
                    self.trigger = True

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Google Speech Recognition API error: {e}")

    def start_listening(self):
        """Start listening in the background."""
        with self.microphone as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source,duration=5)
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
    tts.save("/home/castlebin/code_ws/crash_Lab/mp3_file/output.mps")

    pygame.mixer.init()
    pygame.mixer.music.load("/home/castlebin/code_ws/crash_Lab/mp3_file/output.mps")
    pygame.mixer.music.play()
    
    # while pygame.mixer.music.get_busy():
    #     continue

    # pygame.mixer.quit()

    return None 

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Respeaker USB Mic Array <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def check_parm(dev):
    if dev:
        mic_tuning = Tuning(dev)
        agc_onoff = mic_tuning.read('AGCONOFF')
        freezeonoff = mic_tuning.read('FREEZEONOFF')
        statnoise = mic_tuning.read('STATNOISEONOFF')
        statnoise_sr = mic_tuning.read('STATNOISEONOFF_SR')
        nonstatnoise = mic_tuning.read('NONSTATNOISEONOFF')
        nonstatnoise_sr = mic_tuning.read('NONSTATNOISEONOFF_SR')
        derev_status = mic_tuning.read("RT60ONOFF") #De-reverberation
        aec_status = mic_tuning.read("ECHOONOFF") #aec
        speech_detected = mic_tuning.read("SPEECHDETECTED")
        

        print(f"AGCONOFF: {'On' if agc_onoff == 1 else 'Off'}")
        print(f"FREEZEONOFF: {freezeonoff}")
        print(f"STATNOISEONOFF: {'Enabled' if statnoise == 1 else 'Disabled'}")
        print(f"STATNOISEONOFF_SR: {'Enabled' if statnoise_sr == 1 else 'Disabled'}")
        print(f"NONSTATNOISEONOFF: {'Enabled' if nonstatnoise == 1 else 'Disabled'}")
        print(f"NONSTATNOISEONOFF_SR: {'Enabled' if nonstatnoise_sr == 1 else 'Disabled'}")    
        print(f"De-reverberation (RT60ONOFF): {'Enabled' if derev_status == 1 else 'Disabled'}")
        print(f"Acoustic Echo Cancellation (ECHOONOFF): {'Enabled' if aec_status == 1 else 'Disabled'}")
        print(f"SPEECH_DETECTED: {'Enabled' if speech_detected == 1 else 'Disabled'}")
    else:
        print("Device not found!")

def set_parm(dev):
    if dev:
        mic_tuning = Tuning(dev)
        mic_tuning.write("FREEZEONOFF", 0)
        while True:
            doa_angle = mic_tuning.read("DOAANGLE")
            print(f"Current DOA Angle: {doa_angle}")
            time.sleep(0.1)
            if 89<=int(doa_angle)<91:
                  mic_tuning.write("FREEZEONOFF", 1)
                  break
        mic_tuning.write("AGCONOFF", 1)  # Automatic Gain Control: On
        mic_tuning.write("AGCMAXGAIN", 10.0)  # AGC Maximum gain: 10.0
        mic_tuning.write("STATNOISEONOFF", 1)  # Stationary Noise Suppression: Enabled
        mic_tuning.write("STATNOISEONOFF_SR", 1)  # ASR Stationary Noise Suppression: Enabled
        mic_tuning.write("NONSTATNOISEONOFF", 1)  # Non-Stationary Noise Suppression: Enabled
        mic_tuning.write("NONSTATNOISEONOFF_SR", 1)  # ASR Non-Stationary Noise Suppression: Enabled
        mic_tuning.write("RT60ONOFF", 1)  # De-reverberation: Enabled
        mic_tuning.write("ECHOONOFF", 1)  # Acoustic Echo Cancellation: Enabled
        mic_tuning.write("GAMMAVAD_SR", 5.0)  # Voice Activity Detection 임계값: 5.0
        print("Microphone parameters set successfully.")
        print("\nCurrent Microphone Parameters:")
        parameters_to_check = [
            "DOAANGLE",
            "FREEZEONOFF",
            "AGCONOFF",
            "AGCMAXGAIN",
            "STATNOISEONOFF",
            "STATNOISEONOFF_SR",
            "NONSTATNOISEONOFF",
            "NONSTATNOISEONOFF_SR",
            "RT60ONOFF",
            "ECHOONOFF",
            "GAMMAVAD_SR",
        ]
        
        for param in parameters_to_check:
            try:
                value = mic_tuning.read(param)
                print(f"{param}: {value}")
            except Exception as e:
                print(f"Error reading {param}: {e}")

def audio_initialize():
    atexit.register(sd._terminate)
    sd._initialize()
    

def find_doa(dev):
    if dev:
        Mic_tuning = Tuning(dev)
        print(Mic_tuning.direction)
        while True:
            try:
                print(Mic_tuning.direction)
                time.sleep(1)
            except KeyboardInterrupt:
                break
            
    return Mic_tuning.direction

def vad(dev):
    if dev:
        Mic_tuning = Tuning(dev)
        print(Mic_tuning.is_voice())
        while True:
            try:
                print(Mic_tuning.is_voice())
                time.sleep(1)
            except KeyboardInterrupt:
                break
    return Mic_tuning.is_voice()

def record_audio(filename, duration, samplerate=16000, channels=1):
    print("Recording...")
    sd.default.device = ('ReSpeaker 4 Mic Array (UAC1.0)', None)  # Input Device Setting 
    audio = sd.rec(int(duration * samplerate), samplerate=16000, channels=channels, dtype='int16')
    sd.wait()  
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  
        wf.setframerate(samplerate)
        wf.writeframes(audio.tobytes())
    print(f"Recording saved to {filename}") #Put your file path/file name

def play_audio(filename):
    print(f"Playing {filename}...")
    
    # Initialize pygame mixer
    pygame.mixer.init() 
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    print("Finish.")
    pygame.mixer.quit()
    

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Gpt <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<    

client = OpenAI()
def ask_gpt(prompt):
    try:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
        ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Can't access API;{e}")
        return None
