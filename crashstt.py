import speech_recognition as sr

def find_mic(): # Microphone(device_index=##)
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

def recognize_speech_from_mic_google_free():
    # Voice recognition settings on the microphone
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Voice capture by mic
    with mic as source:
        print("Please enter your voice. . .")
        recognizer.adjust_for_ambient_noise(source)  #Noise correction
        audio = recognizer.listen(source)

    # Attempt to convert voice to text
    try:
        print("Recognizing. . .")
        text = recognizer.recognize_google(audio, language="ko-KR") #Korean recognition, !!50 TIME A DAY!!
        print(f"you said: {text}")
        return text
    except sr.UnknownValueError:
        print("Voice not recognized.")
        return None
    except sr.RequestError as e:
        print(f"Can't access Google API; {e}")
        return None 
    
def recognize_speech_from_mic_google_cloud_speech():
    # Voice recognition settings on the microphone
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Voice capture by mic
    with mic as source:
        print("Please enter your voice. . .")
        recognizer.adjust_for_ambient_noise(source)  #Noise correction
        audio = recognizer.listen(source)
    
    #Attempt to convert voice to text
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
    try:
        print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
