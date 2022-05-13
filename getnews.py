import requests
from pprint import pprint
from keys import NEWS_API_KEY
from datetime import datetime

def get_all_articles(*args):
    all_articles=[]
    for item in args:
        all_articles+=item.json()["articles"]
    return all_articles

def main():
    start_date=datetime.today().strftime('%Y-%m-%d')

    endpoint_top_headlines="https://newsapi.org/v2/top-headlines"
    endpoint_query="https://newsapi.org/v2/everything"

    top_headlines=requests.get(endpoint_top_headlines,params=
                              {"apiKey":NEWS_API_KEY,"country":"us"})
    technology_news=requests.get(endpoint_query,params=
                                {"q":"technology","apiKey":NEWS_API_KEY,"sortBy":"popularity"})

    all_news=get_all_articles(technology_news,top_headlines)
    for news_item in all_news:
        print(news_item["title"])
        print(news_item["description"])
        print(news_item["url"])
        print("\n\n")

if __name__=="__main__":
    main()