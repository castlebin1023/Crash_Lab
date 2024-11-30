import crash_lang as cr
import usb.core #for mic tuning
import usb.util #for mic tuning
import time

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018) #for mic tuning
keywords = ["민준","안내"] 
mic_index = 5 
speech_recognizer = cr.BackgroundSpeechRecognizer(mic_index,keywords)
touch_toggle = False


try:
    cr.audio_initialize()
    cr.set_parm(dev)
    print("Starting background speech recognition...")
    speech_recognizer.start_listening()
    print("Listening in the background")
    
    while True:
        if speech_recognizer.trigger or touch_toggle :
            # print("Start Guide!")
            if speech_recognizer.recognized_text :
                response =cr.ask_gpt(speech_recognizer.recognized_text)
                cr.speak(response,"ko")
                speech_recognizer.recognized_text = None
            # else :
            #     print("No text")
            time.sleep(0.1)
            # speech_recognizer.trigger = False
        pass

except KeyboardInterrupt:
        print("Stopping speech recognition...")
        speech_recognizer.stop_listening(wait_for_stop=True)
        print("Speech recognition stopped.")


