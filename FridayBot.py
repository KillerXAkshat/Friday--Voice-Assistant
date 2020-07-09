import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib 
import random
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
from tkinter import *

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    engine.setProperty("rate",145)
    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour<12:
        speak("Good Morning Boss!")
    elif hour >=12 and hour<18:
        speak("Good Afternoon Boss!")
    else:
        speak("Good Evening Boss!")

    speak("I am Friday. Please tell me how may I help you!")
    
def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=3, phrase_time_limit=3)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language= 'en-in')
        
    except Exception as e:
        print(e)
        engine.setProperty("rate", 120)
        print("Say that again, please...")
        speak("Say that again, please")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email_address', 'your_password')
    server.sendmail('your_email_address', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

         # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            speak(results)
            print(results)

        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com")

        elif 'open google' in query:
            webbrowser.open('www.google.com')
            
        elif 'open coursera' in query:
            webbrowser.open("www.coursera.org")

        elif 'open stackoverflow' in query:
            webbrowser.open("www.stackoverflow.com")

        elif 'open googlecolab' in query:
            webbrowser.open("www.googlecolab.com")

        elif 'spotify' in query:
            os.startfile('C:\\Program Files\\Spotify\\Spotify.exe')     

        elif 'open music player' in query:
         speak("Opening Music Player")
         root = Tk()
         root.minsize(300,300)
         listofsongs = []
         realnames = []
         v = StringVar()
         songlabel = Label(root,textvariable=v,width=35)
         index = 0

         def directorychooser():
             directory = askdirectory()
             os.chdir(directory)
             for files in os.listdir(directory):
                 if files.endswith(".mp3"):
                     realdir = os.path.realpath(files)
                     audio = ID3(realdir)
                     realnames.append(audio['TIT2'].text[0])
                     listofsongs.append(files)
             pygame.mixer.init()
             pygame.mixer.music.load(listofsongs[0])
             #pygame.mixer.music.play()
         directorychooser()

         def updatelabel():
             global index
             global songname
             v.set(realnames[index])
             #return songname

         def nextsong(event):
             global index
             index += 1
             pygame.mixer.music.load(listofsongs[index])
             pygame.mixer.music.play()
             updatelabel()

         def prevsong(event):
             global index
             index -= 1
             pygame.mixer.music.load(listofsongs[index])
             pygame.mixer.music.play()
             updatelabel()

         def stopsong(event):
             pygame.mixer.music.stop()
             v.set("")
             #root.destroy()
            #return songname
        
         def quitplayer(event):
             pygame.mixer.music.stop()
             v.set("")
             root.destroy()

         label = Label(root,text='Music Player')
         label.pack()

         listbox = Listbox(root)
         listbox.pack()

         #listofsongs.reverse()
         realnames.reverse()

         for items in realnames:
             listbox.insert(0,items)

         realnames.reverse()
        #listofsongs.reverse()

         nextbutton = Button(root,text = 'Next Song')
         nextbutton.pack()
 
         previousbutton = Button(root,text = 'Previous Song')
         previousbutton.pack()

         stopbutton = Button(root,text='Stop Music')
         stopbutton.pack()
         
         quitbutton = Button(root,text = "Quit")
         quitbutton.pack()
         
         nextbutton.bind("<Button-1>",nextsong)
         previousbutton.bind("<Button-1>",prevsong)
         stopbutton.bind("<Button-1>",stopsong)
         quitbutton.bind("<Button-1>",quitplayer)
         songlabel.pack()
         root.mainloop()
    
        elif 'send email' in query:
            try:
                speak('What should I say?')
                content = takeCommand()
                to = "your_email_address"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Boss, I am not able to send this email")    

        elif 'exit' in query:    
            speak("Thank you for using me, have a nice day")    
            exit()