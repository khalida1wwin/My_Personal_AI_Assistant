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
# Done: it can change voice gender
# Done: it can look up synonyms
# Done: Look up whether

# TODO: add cv2 and mediapipe functions
# TODO: it needs to remember the old settings like name
# TODO: Automated web scraping
import requests
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from nltk.corpus import wordnet
import nltk
import cv2
import time
import HandTrackingModule as htm
import requests
import os


class AI:
    def __init__(self):
        # Strings Init
        self.AI_Name = "alexa"
        self.GeneralCommands = "start of conversation"
        self.yesWordsList = self.get_all_word_synonyms('ok') + self.get_all_word_synonyms(
            "yes") + self.get_all_word_synonyms('yea') + ['yes']
        # Cam Init
        self.time = time
        self.wCam, self.hCam = 640, 480
        self.CamNumber = 1
        self.cap = cv2.VideoCapture(self.CamNumber)
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)

        # Voice recognition Init
        self.listener = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.typeOfVoice = 1
        self.engine.setProperty('voice', self.voices[self.typeOfVoice].id)
        self.engine.say('Hi I am listening ')
        self.engine.runAndWait()  # you need this to let the engine have time to speak

    def download_nltk_dependencies_if_needed(self):
        try:
            nltk.word_tokenize('foobar')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.pos_tag(nltk.word_tokenize('foobar'))
        except LookupError:
            nltk.download('averaged_perceptron_tagger')

    def get_some_word_synonyms(self, word):
        word = word.lower()
        synonyms = []
        synsets = wordnet.synsets(word)
        if (len(synsets) == 0):
            return []
        synset = synsets[0]
        lemma_names = synset.lemma_names()
        for lemma_name in lemma_names:
            lemma_name = lemma_name.lower().replace('_', ' ')
            if (lemma_name != word and lemma_name not in synonyms):
                synonyms.append(lemma_name)
        return synonyms

    def get_all_word_synonyms(self, word):
        word = word.lower()
        synonyms = []
        synsets = wordnet.synsets(word)
        if (len(synsets) == 0):
            return []
        for synset in synsets:
            lemma_names = synset.lemma_names()
            for lemma_name in lemma_names:
                lemma_name = lemma_name.lower().replace('_', ' ')
                if (lemma_name != word and lemma_name not in synonyms):
                    synonyms.append(lemma_name)
        return synonyms

    def take_command(self, listeningFor):
        '''
            This function listen to the user and returns their input
            '''
        command = ''
        while True:
            try:
                with sr.Microphone() as source:
                    print("speak now..." + listeningFor)

                    voice = self.listener.listen(source)
                    command = self.listener.recognize_google(voice)
                    command = command.lower()


            except:
                pass
            else:
                break

        return command

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def run_AI(self):
        command = self.take_command(self.GeneralCommands)
        if self.AI_Name in command:
            command = command.replace(self.AI_Name, '')
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

            elif "synonym word for" in command:

                synonymWord = command.split("synonym word for", 1)[1]
                print("word is", synonymWord)
                listOfSynonmys = self.get_all_word_synonyms(synonymWord.strip())  # need to get rid off-white space or
                # it will not work
                print(listOfSynonmys)
                for word in listOfSynonmys:
                    print(word)
                    self.talk(word)
            elif "change your voice to" in command:
                newVoicetype = command.split("change your voice", 1)[1]
                femaleSynonym = self.get_all_word_synonyms("female") + ["female"]
                malesynonym = self.get_all_word_synonyms("male") + ["male"]
                print("word is", newVoicetype)
                print(femaleSynonym)
                print(malesynonym)
                if any(word in newVoicetype.strip() for word in femaleSynonym):
                    self.typeOfVoice = 1
                    print(self.typeOfVoice)
                    self.engine.setProperty('voice', self.voices[self.typeOfVoice].id)
                elif any(word in newVoicetype.strip() for word in malesynonym):
                    self.typeOfVoice = 0
                    print(self.typeOfVoice)
                    self.engine.setProperty('voice', self.voices[self.typeOfVoice].id)
            elif "weather" in command:
                city = "Edmonton"
                url = 'https://wttr.in/{}'.format(city)
                res = requests.get(url)
                self.talk("this is the waether for" + city)
                print(res.text)


            elif "cam" in command:
                pTime = 0
                decorator = htm.handDetector(trackCon=0.7)  # confidence of the detection
                # if "quit" in self.take_command("quit"):
                # # break
                tipIDs = [4, 8, 12, 16, 20]
                bestOutOf = 1
                self.talk("best out of three?")
                answer = self.take_command("RPS")
                if answer in self.yesWordsList:
                    bestOutOf = 3
                while True:
                    success, img = self.cap.read()
                    img = decorator.findHands(img)
                    cTime = self.time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime
                    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

                    fingers = []
                    lmList = decorator.findPosition(img, draw=False)
                    if len(lmList) != 0:

                        if lmList[tipIDs[0]][1] > lmList[tipIDs[0] - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                        for id in range(1, 5):
                            if lmList[tipIDs[id]][2] < lmList[tipIDs[id] - 2][2]:
                                fingers.append(1)
                            else:
                                fingers.append(0)

                    TotoalFingers = fingers.count(1)
                    print(TotoalFingers)
                    # print(fingers)
                    cv2.rectangle(img, (20, 270), (170, 300), (0, 0, 0), cv2.FILLED)
                    # 0 fingers up means rock
                    if TotoalFingers == 0:
                        cv2.putText(img, "Rock", (30, 290), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
                    # 2 fingers up means Scissors
                    elif TotoalFingers == 2:
                        cv2.putText(img, "Scissors", (30, 290), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
                    # 5 fingers up means Paper
                    elif TotoalFingers == 5:
                        cv2.putText(img, "Paper", (30, 290), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

                    cv2.rectangle(img, (570, 50), (630, 0), (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, "X", (570, 50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3)

                    # index finger pos
                    if len(lmList) != 0:

                        x1 , y1 = lmList[8][1], lmList[8][2]


                        if (x1 > 570) and (y1 <50 ):
                            cv2.destroyAllWindows()
                            break

                    # k = cv2.waitKey(0)
                    # if k == 27:  # wait for ESC key to exit and terminate progra,
                    #     cv2.destroyAllWindows()
                    #     break
                    # # if "quit" in self.take_command("quit"):
                    # #     break

                    cv2.imshow("Image", img)
                    cv2.waitKey(1)
            else:
                self.talk('sorry I did not understand')

AI = AI()
while True:
    AI.run_AI()


