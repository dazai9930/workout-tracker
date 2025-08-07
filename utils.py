import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
        if 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()
