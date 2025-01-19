from ipaddress import ip_address  # This import is not used in the code
import pyttsx3  # pyttsx3 converts text to speech
import speech_recognition as sr  # recognizes speech from user
import keyboard
import os
import subprocess as sp
from datetime import datetime
from decouple import config  # for fetching user and bot variables
from random import choice

from pyexpat.errors import messages

from conv import random_text  # Ensure this is defined correctly
from online import find_my_ip
from online import search_on_google
from online import search_on_wikipedia
from online import youtube , get_news

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')  # sapi5 is used for speech recognition
engine.setProperty('volume', 1.0)  # Volume should be between 0.0 and 1.0
engine.setProperty('rate', 225)
voices = engine.getProperty('voices')  # this variable includes voices of python library
engine.setProperty('voice', voices[1].id)  # Set to a specific voice

USER = config('USER')
HOSTNAME = config('BOT')

def speak(text):
    engine.say(text)  # includes text
    engine.runAndWait()  # wait for user input

def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USER}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good Afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USER}")
    else:
        speak(f"Good Night {USER}")
    speak(f"I am {HOSTNAME}. How may I assist you?")

listening = False

def start_listening():
    global listening
    listening = True
    print("Started listening")

def pause_listening():
    global listening
    listening = False
    print("Stopped listening")

# Set up hotkeys
keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1  # wait for user input voice
        audio = r.listen(source)  # Capture the audio input

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-IN')  # Corrected language code
            print(query)
            return query
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Can you please repeat that?")
            return "None"
        except sr.RequestError:
            speak("Sorry, there was an error with the speech recognition service.")
            return "None"

if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine. What about you?")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                sp.Popen('cmd.exe')  # This will open the Command Prompt

            elif "open camera" in query:
                speak("Opening camera")
                os.startfile("microsoft.windows.camera:")

            elif "open notepad" in query:
                speak("Opening notepad for you")
                notepad_path = r"C:\Users\grish\OneDrive\Desktop\Notepad.lnk"  # Use raw string
                os.startfile(notepad_path)

            elif "ip address" in query:
                user_ip = find_my_ip()  # Renamed variable to avoid conflict
                speak(f"Your IP address is {user_ip}")
                print(f"Your IP address is {user_ip}")

            elif "open youtube" in query:
                speak("What do you want to play on YouTube?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak("What do you want to search?")
                query = take_command().lower()
                search_on_google(query)  # Fixed typo

            elif "wikipedia" in query:
                speak("What do you want to search?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to Wikipedia, {results}")
                print(results)  # Print the actual results

            elif "send an email" in query:
                speak("on what email address do you wan to send , pleasw enter in the terminal")
                reciever_add = input("Email address:")
                speak("what should be the subject")
                subject = take_command().capitalize()
                speak("what is the message")
                message =  take_command().capitalize()
                if send_email(reciever_add,subject,message):
                    speak("I have send the mail")
                    print("I have send the mail")


            elif "give me news" in query:

                speak("I am reading out the latest headlines for today.")
                speak(get_news())
                speak("i am printing it on screen")
                print(*get_news(),sep='\n')

                # news_headlines = get_news()  # Ensure this returns a list of headlines
                #
                # if news_headlines:
                #     for headline in news_headlines:
                #         speak(headline)  # Speak each headline
                #         print(headline)  # Print each headline

                # else:
                #     speak("Sorry, I couldn't fetch the news at the moment.")
        else:
                speak("something went wrong ")
                break  # Exit the loop

