from gtts import gTTS
import speech_recognition as sr
import sys
from exitstatus import ExitStatus
import re
import webbrowser
import requests
import pyttsx3
from selenium import webdriver
import winsound
import vlc
import os

#for audio
def talkToMe(audio):

    print(audio)
    engine = pyttsx3.init()
    sound = engine.getProperty('voices')
    engine.setProperty('voice', sound[1].id)#for female voice
    engine.say(audio)
    engine.runAndWait()

#to listen commands
def myCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        talkToMe('Your last command couldn\'t be heard. Try again')
        command = myCommand();

    return command


def assistant(command):
    #if statements for executing commands

    if 'what\'s up' in command:
        talkToMe('Just doing my thing')

    elif 'hey' in command:
        talkToMe('Hello. How may I help you?')
        
    #To open a folder on desktop
    elif 'open folder' in command:
        reg_ex = re.search('open folder (.*)',command)
        if reg_ex:
            folder = reg_ex.group(1)
            webbrowser.open("C:\\Users\\Sanika Sanaye\\Desktop\\"+folder)
            talkToMe('What should I do next?')
            key2 = myCommand()

            #To create folder in current folder
            if 'create' in key2:
                reg_ex = re.search('create (.*)', key2)
                if reg_ex:
                    subfolder = reg_ex.group(1)
                    os.mkdir("C:\\Users\\Sanika Sanaye\\Desktop\\"+folder+"\\"+subfolder)

            #To remove folder from current folder
            elif 'remove' in key2:
                reg_ex = re.search('remove (.*)', key2)
                if reg_ex:
                    subfolder = reg_ex.group(1)
                    os.rmdir("C:\\Users\\Sanika Sanaye\\Desktop\\"+folder+"\\"+subfolder)
                    
            talkToMe('Done')
        
    #To open YouTube   
    elif 'open youtube' in command:
        url = 'https://www.youtube.com/'
        webbrowser.open(url)
        talkToMe('What would you like to do next')
        key = myCommand()
        if 'search for' in key:
                     reg_ex = re.search('search for (.*)', key)
                     url = 'https://www.youtube.com/results?search_query='
                     if reg_ex:
                         search = reg_ex.group(1)
                         url = url + search
                         webbrowser.open_new_tab(url)
                     talkToMe('Done')

    #To google search something
    elif 'google search' in command:
                     reg_ex = re.search('google search (.*)', command)
                     url = 'https://www.google.com/search?q='
                     if reg_ex:
                         search = reg_ex.group(1)
                         url = url + search
                         webbrowser.open(url)
                     talkToMe('Done')
    
    #To open a website                 
    elif 'open' in command:
        
        reg_ex = re.search('open (.*)', command)
        if reg_ex:
            website = reg_ex.group(1)
            webbrowser.open("https://www."+website+".com")
                     
    #To tell current weather in a city in india           
    elif 'current weather in' in command:
        driver = webdriver.Chrome()
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            driver.get("https://www.euronews.com/weather/asia/india/"+city)
        talkToMe('The current weather in %s is %s' %(city,driver.find_element_by_xpath("//*[@class='unit_C enw-block__cityWeather__forecast__desc ltr no-unit']").text))


    #To play music
    elif 'play music' in command:
        p = vlc.MediaPlayer("C:\\Users\\Sanika Sanaye\\Downloads\\MAMAMOO_-_Sleep_In_The_Car_(mp3.pm).mp3")
        p.play()
        print("press 1 to close music")
        key1 = input()
        if '1' in key1:
           p.stop()

    
    #To exit the program
    elif 'exit' in command:
        talkToMe('Thanks Sanika. See you next time')
        sys.exit(ExitStatus.success)
        
    #when a command doesn't match any given commands
    else:
            talkToMe('I don\'t know what you mean!')


talkToMe('Welcome to your desktop assistant.')
talkToMe("1. What's up\n2. Hey\n3. Open Folder\n  3.1. Create\n  3.2. Remove\n4. Open YouTube\n  4.1. Search for\n5. Google Search\n6. Open\n7. Current Weather in City\n8. Play Music\n9. Exit\n")
talkToMe("How may I help you?")

#loop to continue executing
while True:
    assistant(myCommand())
