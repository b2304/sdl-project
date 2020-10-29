import pyttsx3
import datetime
import speech_recognition as sr 
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os
import pyautogui
import random
import json
import requests
from urllib.request import urlopen
import wolframalpha
import time

engine = pyttsx3.init()

wolframalpha_app_id = '4Y77LR-V5AVLK362L'

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time = datetime.datetime.now().strftime("%H:%M:%S")  #for 24 hour clock
    #Time = datetime.datetime.now().strftime("%I:%M:%S")  #for 12 hour clock
    speak("The current time is ")
    speak(Time)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    date = datetime.datetime.now().day
    speak("The current date is ")
    speak(date)
    speak(month)
    speak(year)


def wishme():
    speak("Welcome back Bhagyashree!")
    time_()
    date_()

    #Greetings

    hour = datetime.datetime.now().hour
    if hour>=6 and hour<12:
        speak("Good Morning...")
        speak("Have a good day!!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!!")
    elif hour>=18 and hour<24:
        speak("Good Evening!!")
    else:
        speak("Good Night..")

    speak("Jarvis at your service. How can I help you??")

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-US')
        print(query)

    except Exception as e:
        print(e)
        print("Say that again please...")
        #speak("Can't recognize.Say that again please...")
        return "None"
    return query

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()

    server.login('username@gmail.com','password')
    server.sendmail('username@gmail.com', to, content)
    server.close()


def screenshot():
    img = pyautogui.screenshot()
    img.save("C:\\Users\\Bhagyashree Waghmare\\Desktop\\screenshot.png")

def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at'+usage)

    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(battery.percent)

def joke():
    speak(pyjokes.get_joke())

if __name__ == "__main__":
    
    wishme()

    while True:
        query = TakeCommand().lower()

        if 'time' in query: #tell us time when asked
            time_()
        
        elif 'date' in query:
            date_()

        elif 'wikipedia' in query:
            speak("Searching...")
            query = query.replace('wikipedia','')
            result = wikipedia.summary(query,sentences=4)
            speak("According to Wikipedia...")
            print(result)
            speak(result)
        
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = TakeCommand()

                #receiver = 'receiver_is_me@gmail.com'

                speak("Who is the Receiver?")
                reciever = input("Enter Receiver Email: ")
                to = reciever
                sendEmail(to,content)
                speak(content)
                speak("Email has been sent.")

            except Exception as e:
                print(e)
                speak("Sorry!!!Unable to send Email.")

        elif 'search in chrome' in query:
            speak("What should I search?")
            chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

            search = TakeCommand().lower()
            wb.get(chromepath).open_new_tab(search+'.com')

        elif 'search youtube' in query:
            speak("What should I search?")
            search_Term = TakeCommand().lower()
            speak("Here we go to YOUTUBE!")
            wb.open('https://www.youtube.com/results?search_query='+search_Term)

        elif 'search google' in query:
            speak("What should I search?")
            search_Term = TakeCommand().lower()
            speak("Searching....")
            wb.open('https://www.google.com/search?q='+search_Term)

        elif 'open stack overflow' in query:
            wb.open("https://www.stackoverflow.com/")   

        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            joke()

        elif 'go offline' in query:
            speak("Going offline master!")
            quit()

        elif 'word' in query:
            speak("Opening MS Word...")
            ms_word = r'C:\Program Files (x86)\Microsoft Office\Office14\WINWORD.EXE'
            os.startfile(ms_word)

        elif 'write a note' in query:
            speak("What should I write?")
            notes = TakeCommand()
            file = open('notes.txt','w')
            speak("Do you want to include Date and Time?")
            ans = TakeCommand()
            if 'yes' in ans or 'sure' in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(':-')
                file.write(notes)
                speak("Done taking notes.")
            else:
                file.write(notes)

        elif 'show notes' in query:
            speak("Showing notes")
            file = open('notes.txt','r')
            print(file.read())
            speak(file.read())

        elif 'screenshot' in query:
            screenshot()

        elif 'play music' in query:
            songs_dir = 'D:\\video songs'
            music = os.listdir(songs_dir)
            speak("What to play?")
            ans = TakeCommand().lower()
            while('number' not in ans and ans != 'random' and ans!='you choose'):
                speak("I could not understand you..Please try again..")
                ans = TakeCommand().lower()
            if 'number' in ans:
                no = int(ans.replace('number',''))
            if 'random' or 'you choose' in ans:
                no = random.randint(1,100)

            os.startfile(os.path.join(songs_dir,music[no]))

        elif 'remember that' in query:
            speak("What should I remember?")
            memory = TakeCommand()
            speak("You asked me to remember"+memory)
            remember = open('memory.txt','w')
            remember.write(memory)
            remember.close()

        elif 'do you remember something' in query:
            remember = open('memory.txt','r')
            speak('You asked me to remember that'+remember.read())

        elif 'news' in query:
            try:
                jsonObj = urlopen("http://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey=9f992c3232a145f39a76efc28774c4b2")
                data = json.load(jsonObj)
                i = 1

                speak('Here are some top headlines from Entertainment Industry')
                print('===========TOP HEADLINES=========='+'\n')
                for item in data['articles']:
                    print(str(i)+', '+item['title']+'\n')
                    print(item['description']+'\n')
                    speak(item['title'])
                    i += 1

            except Exception as e:
                print(str(e))

        elif 'where is' in query:
            query = query.replace("where is","")
            location = query
            speak("Locate"+location)
            wb.open_new_tab("https://www.google.com/maps/place/"+location)

        elif 'calculate' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(''.join(query))
            answer = next(res.results).text 
            print("Answer is : "+answer)
            speak("Answer is "+answer)

        elif 'what is' in query or 'who is' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            res = client.query(query)

            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print("No Results")

        elif 'stop listening' in query:
            speak("For how many seconds you want me to stop listening to your commands?")
            ans = int(TakeCommand())
            time.sleep(ans)
            print(ans)

        elif 'log out' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")