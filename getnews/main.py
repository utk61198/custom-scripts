import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv
from deta import app
load_dotenv()
import os


def get_all_articles(*args):
    all_articles=[]
    for item in args:
        all_articles+=item.json()["articles"]
    return all_articles





@app.lib.cron()
def main(event):
    sender_address = 'utkarsh.py.automation@gmail.com'
    sender_pass = os.environ.get('EMAIL_PASSWORD')
    receiver_address = 'utk61198@gmail.com'
    NEWS_API_KEY=os.environ.get('NEWS_API_KEY')

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Daily news feed'

    start_date=datetime.today().strftime('%Y-%m-%d')
    # add more endpoints to customize the type of news

    endpoint_top_headlines="https://newsapi.org/v2/top-headlines"
    endpoint_query="https://newsapi.org/v2/everything"

    top_headlines=requests.get(endpoint_top_headlines,params=
                              {"apiKey":NEWS_API_KEY,"country":"us"})
    technology_news=requests.get(endpoint_query,params=
                                {"q":"technology","apiKey":NEWS_API_KEY,"sortBy":"popularity"})

    all_news=get_all_articles(top_headlines,technology_news)
    mail_body=""
    for news_item in all_news:
        mail_body+=str(news_item["title"])+"\n\n"
        mail_body+=str(news_item["description"])+"\n"
        mail_body+=str(news_item["url"])+"\n\n\n"

    message.attach(MIMEText(mail_body, 'plain'))
    text=message.as_string()
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address,sender_pass)
    session.sendmail(sender_address,receiver_address,text)
    session.quit()


if __name__=="__main__":
    main()
