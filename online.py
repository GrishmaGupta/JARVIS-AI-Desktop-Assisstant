from ipaddress import ip_address

import requests
import wikipedia
import pywhatkit as kit #used to access online function slike google ,yt
from email.message import EmailMessage
import smtplib
from decouple import config

EMAIL =""
Password = ""

def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query,sentences=2)
    return results

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.playonyt(video)

def send_email(reciever_add,subject,message):
    try:
        email = EmailMessage()
        email['To'] = reciever_add
        email['subject'] = subject
        email['From'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL,Password)
        s.send_message(email)
        s.close()
        return True

    except Exception as e:
        print(e)
        return False

def get_news():
    news_headline = []
    result = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey=ea72ae3cbac0477187bd9f6795b3c26c").json()

    articles = result["articles"]
    for article in articles:
        news_headline.append(article['title'])
        return news_headline[:6]
