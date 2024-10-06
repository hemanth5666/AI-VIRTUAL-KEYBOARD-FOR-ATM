import pyttsx3

def talk(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
