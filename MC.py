import google.generativeai as genai
import time
import sys
import Speech_rec as sr
import webbrowser as wb
import json
import random
import os
import smtplib
import requests
from pprint import pprint
from selenium import webdriver 
from subprocess import Popen, PIPE
import requests
import threading
import psutil
import keyboard
from sumy.summarizers.lsa import LsaSummarizer 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer                 

          

GOOGLE_API_KEY='AIzaSyB2z2ZX0A2zM4QYxh9FkjvUGIoxoTfskpU'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def StartChat():
    speak("initialising AI chat...")
    speak("initialised..")
    return model.start_chat(history=[]) #Start a new chat

def game_idea():
    j = json.loads(open('information.json').read())
    
    def getRandomItem(items):
        return items[random.randint(0, len(items) - 1)]
    
    def getIdea():
        mood = getRandomItem(j["mood"])
        theme1 = getRandomItem(j["theme"])
        random.seed()
        theme2 = getRandomItem(j["theme"])
        genre1 = getRandomItem(j["genre"])
        random.seed()
        genre2 = getRandomItem(j["genre"])
        perspective = getRandomItem(j["perspective"]);
        character = getRandomItem(j["character"]["description"]) + ' ' + getRandomItem(j["character"]["nature"]) + ' ' + getRandomItem(j["character"]["description_post"])
        setting = getRandomItem(j["settings"]["place"]).format(description = getRandomItem(j["settings"]["description"]))
        goal = getRandomItem(j["goal"])
        wildcard = getRandomItem(j["wildcard"])
    
        return getRandomItem(j["template"]).format(mood = mood,
                                                  theme1 = theme1,
                                                 theme2 = theme2,
                                                 perspective = perspective,
                                                genre1 = genre1,
                                                genre2 = genre2,
                                               character = character,
                                              setting = setting,
                                              wildcard = wildcard,
                                              goal = goal)
    
    Idea = getIdea()

    print(Idea)
    transcribe_answers(Idea)
    speak(Idea)


def speak(text):
    if sys.platform.startswith('darwin'):
        from  AppKit import NSSpeechSynthesizer
        nssp = NSSpeechSynthesizer
        ve = nssp.alloc().init()
        ve.setVoice_("com.apple.voice.compact.en-GB.Daniel")
        ve.startSpeakingString_(text)
        while not ve.isSpeaking():
          time.sleep(0.1)

        while ve.isSpeaking():
          time.sleep(0.1)
    else:
        #for windows
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)     # setting up new voice rate
        engine.setProperty('volume', 1.0)   # settin up the volume
        voices = engine.getProperty('voices')       #getting details of current voice
        engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for male , 0 for female

        engine.say(text)
        engine.runAndWait()


def listener():
    speech = sr.listen()
    return speech
    

def summarize(text, language="english", sentences_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return ' '.join([str(sentence) for sentence in summary])


def Quit():
    speak("ok sir shutting down the system")
    quit()

def run_wake():
    global awoken, memory
    awoken = False
    wakeup = None

    while True:
        wakeup = listener().lower()
        if 'hey mc' in wakeup:
            chat = StartChat()
            while True:
                run_alexa(chat)
        elif 'hi mc' in wakeup:
            chat = StartChat()
            while True:
                
                run_alexa(chat)  
        elif 'shut down' in wakeup:
            Quit()

def sleep_mode():
    while True:
        wakeup = listener().lower()
        if 'hey mc' in wakeup:
            while True:
                run_alexa(chat)
        elif 'hi mc' in wakeup:
            while True:
                run_alexa(chat)  

def transcribe_answers(response):
    f = open("logs.txt", "a")
    f.write("\n\n-----------------------------------------------------------------------------------------------------------\n\n")
    print(response, file=f)
    f.close()

def memory_(response, type):
    f = open("seperate.txt", "a")  
    n = response.split("```")
    l = len(n)/3
    i = 0
    while l > 0:
        n.pop(i)
        n.pop(i+1)
        i = i + 1
        l= l - 1
    intry = (' '.join(n))
    f.write(intry)
    f.close()




def run_alexa(chat):
    global awoken, memory
    if not awoken:
        speak("How can I help you today sir")
        awoken = True
    else:
        speak("Can I help you with anything else sir")
    command = listener().lower()
    if 'shut down' in command:
        Quit()
    elif 'sleep' in command:
        sleep_mode()
    elif 'offline' in command:
        if 'game idea' in command:
            game_idea()
    elif 'seperate' in command:
        if 'code' in command:
            memory_(memory, "code")
        else:
            speak("what should I seperate sir.")
            seperate = listener().lower()
            if 'code' in seperate:
                memory_(memory, "code")
        
    else:
        response = chat.send_message(command)
    # Summarize using sumy LSA  
    print(response.text)        
    transcribe_answers(response.text)    
    summery = summarize(response.text) 
    speak(summery + " for more information check the logs file sir.")
    memory = response.text


run_wake()