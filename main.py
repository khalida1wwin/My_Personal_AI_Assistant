
# things to you might face if you try making this project
# 1.solved pyAudio not supporting newer versions of python from here
# https://stackoverflow.com/questions/61348555/error-pyaudio-0-2-11-cp38-cp38-win-amd64-whl-is-not-a-supported-wheel-on-this-p
# run this in the project venv
#pip install pipwin
#pipwin install pyaudio
# 2. solved engine = pyttsx3.init() error from here
#https://stackoverflow.com/questions/61348555/error-pyaudio-0-2-11-cp38-cp38-win-amd64-whl-is-not-a-supported-wheel-on-this-p
# just lower pyttsx3 to 2.71
#3 solve pywhatkit import error from here
#https://stackoverflow.com/questions/31252791/flask-importerror-no-module-named-flask
#pip install flask
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
listener = sr.Recognizer()

# voice = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.say('Hi I am listening ')
engine.runAndWait() # you need this to let the engine have time to speak


AI_Name = 'L'

def take_command():
    def talk(text):
        engine.say(text)
        engine.runAndWait()

    try:
        with sr.Microphone() as source:
            print("speak now...")

            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

            if AI_Name in command:
                command = command.replace(AI_Name, '')
                print(command)
    except:
        pass

    return command
def talk(text):
    engine.say(text)
    engine.runAndWait()

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play','')
        talk('playing' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk("it's " + time)
    elif 'who' in command:
        person = command.replace('who','')
        info = wikipedia.summary(person,1) # summary takes the info to be searched and number of lines of the answer
        print(info)
        talk(info)
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)
    else:
        talk('sorry I did not understand')


while True:
    run_alexa()