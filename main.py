# things to you might face if you try making this project
# 1.solved pyAudio not supporting newer versions of python from here
# https://stackoverflow.com/questions/61348555/error-pyaudio-0-2-11-cp38-cp38-win-amd64-whl-is-not-a-supported-wheel-on-this-p
# run this in the project venv
# pip install pipwin
# pipwin install pyaudio
# 2. solved engine = pyttsx3.init() error from here
# https://stackoverflow.com/questions/61348555/error-pyaudio-0-2-11-cp38-cp38-win-amd64-whl-is-not-a-supported-wheel-on-this-p
# just lower pyttsx3 to 2.71
# 3 solve pywhatkit import error from here
# https://stackoverflow.com/questions/31252791/flask-importerror-no-module-named-flask
# pip install flask

# Done: it tells time
# Done: it tells a joke
# Done: it plays music on YouTube


# TODO: it needs to remember the old settings like name
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes


class AI():
    def __init__(self):
        self.AI_Name = "alexa"
        self.GeneralCommands = "start of conversation"
        self.yesWordsList = ["yes", "yep", "sure", "yea"]
        self.listener = sr.Recognizer()
        # voice = engine.getProperty('voices')
        # engine.setProperty('voice', voices[1].id)
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.say('Hi I am listening ')
        self.engine.runAndWait()  # you need this to let the engine have time to speak

    def take_command(self, listeningFor):
        '''
        This function listen to the user and returns their input
        '''

        def talk(text):
            self.engine.say(text)
            self.engine.runAndWait()

        try:
            with sr.Microphone() as source:
                print("speak now..." + listeningFor)

                voice = self.listener.listen(source)
                command = self.listener.recognize_google(voice)
                command = command.lower()


        except:
            pass

        return command

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def run_AI(self):
        command = self.take_command(self.GeneralCommands)
        if self.AI_Name in command:
            command = command.replace(self.AI_Name, '')
            print(command)
            print(command)
            if 'play' in command:
                song = command.replace('play', '')
                self.talk('playing' + song)
                pywhatkit.playonyt(song)

            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                print(time)
                self.talk("it's " + time)
            elif 'who' in command:
                person = command.replace('who', '')
                info = wikipedia.summary(person,
                                         1)  # summary takes the info to be searched and number of lines of the answer
                print(info)
                self.talk(info)
            elif 'joke' in command:
                joke = pyjokes.get_joke()
                print(joke)
                self.talk(joke)
            elif "what's your name" in command:
                self.talk("my name is " + self.AI_Name)
                self.talk("if you want to change it, say I want to change your name")
            elif "change your name" in command:
                self.talk("okay say what is my new name")
                name = self.take_command("listen for new name")
                print(name)
                answer = ""
                for i in range(2):
                    if answer not in self.yesWordsList:
                        self.talk("do you want to change my name form " + self.AI_Name + " to " + name)
                        answer = self.take_command("change AI Name")
                    else:
                        self.AI_Name = name
                        self.talk("My new name is " + name)
                        break
                    if i == 1:
                        self.talk("My name is still" + self.AI_Name)

            else:
                self.talk('sorry I did not understand')


AI = AI()
while True:
    AI.run_AI()
