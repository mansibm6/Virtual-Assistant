# Description: This is a virtual assistant program that gets date, time, responds with a random
# greeting and returns information on a person if asked(both first and last name needed)

# Package Requirements: pyaudio, Speechrecognition, gTTS, wikipedia
import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

warnings.filterwarnings('ignore')
#function to record audio and return it as string
def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something: ")
        audio=r.listen(source)
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)

    except sr.UnknownValueError:
        print("Couldn't recognize audio")
    except sr.RequestError as e:
        print("Google speech recognition error")
    return data

#function to get virtual assistant response
def assistantResponse(text):
    print(text)
    myobj = gTTS(text= text, lang= 'en', slow=False)
    myobj.save('assistant_response.mp3') #saving the audio file
    os.system('start assistant_response.mp3')

#function for wake word or phrase
def wakeWord(text):
    WAKE_WORD = ['hello computer']
    text=text.lower() #converting to lower case as wake words are lower case
    for phrase in WAKE_WORD:
        if phrase in text:
            return True

    return False #returns False if wake word not found

#function to get date
def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December' ]
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']
    return 'Today is '+ weekday+ " " + month_names[monthNum-1]+' the '+ordinalNumbers[dayNum-1]+'.'

#function to return a random greeting
def greeting(text):
    GREETING_INPUTS=['hi', 'hey', 'hola', 'hello']
    GREETING_RESPONSES=['hello Mansib']
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'
    return ''

#function to get a person's first and last name
def getPerson(text):
    wordList=text.split()
    for i in range(0, len(wordList)):
        if i+3<=len(wordList)-1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' ' + wordList[i+3]

while True:
    text = recordAudio()
    response = ''
    if(wakeWord(text)== True):
        response = response + greeting(text)
        if ('date' in text):
            get_date=getDate()
            response=response+' '+ get_date
        if('time' in text):
            now=datetime.datetime.now()
            meridiem = ''
            if now.hour >= 12:
                meridiem='p.m'
                hour=now.hour - 12
            else:
                meridiem='a.m'
                hour=now.hour
                if now.minute < 10:
                    minute='0'+str(now.minute)
                else:
                    minute=str(now.minute)
                response=response+' '+"It is"+ str(hour)+':'+minute+' '+meridiem+" ."


        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response=response+' '+wiki
        assistantResponse(response)