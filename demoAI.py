"""
Note : Cant use Speak(audio) in this package
    Return the string we want to say aloud to demoApp.py then use speak(audio) by importing method.
    Speed Test Intallation = pip install speedtest-cli
        from speedtest import *
        stObj = SpeedTest()
        print(st.download(), st.upload())
    1. Add more songs in Static File and select random songs using random module
    2. use try except block
    3. implement Amazon, Youtube, Search Query 
"""

import datetime
from bs4.builder import HTML
from tts2 import *
from speedtest import *
import azure.cognitiveservices.speech as sr
import wikipedia
from bs4 import *
import webbrowser
import wolframalpha
import random
import requests
import json
import os
import torch
from brain import NeuralNet
from NeuralNetwork import bag_of_words , tokenize

appId = "ad2706636ddfcf6579b8e07d682d9e68"
clientObj = wolframalpha.Client("QAY9L8-W7G3WGJ875")  # Wolframe API Key
e1 = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
# e1.setProperty("voice", e1.getProperty("voices")[0].id)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intents.json",'r') as json_data:
    intents = json.load(json_data)

FILE = "TrainData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]
model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def speak(audio):
    e1.result(audio)
    e1.runAndWait()


def greet(name):#rakna hai
    getTime = datetime.datetime.now().hour
    if getTime >= 0 and getTime < 12:
        return f"Good Morning {name}"

    elif getTime >= 12 and getTime < 18:
        return f"Good Afternoon {name}"

    else:
        return f"Good Evening {name}"


def takeCommand():  
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8  # default is 0.8
        r.energy_threshold = 200  # default is 300
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")

    except Exception:   #in any case of On Internet
        # print(e)
        print("Say that again please...")
        return "None"

    return query.lower()


def working(query):     #user input will be compare by each task
    sentence = query

    if sentence == "bye":
        exit()
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1,X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)

    _ , predicted = torch.max(output,dim= 1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output,dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                reply = random.choice(intent["responses"])
                speak(reply)



