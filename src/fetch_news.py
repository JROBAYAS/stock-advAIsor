import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_company_news(ticker, company_name):
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={company_name}&language=es&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url).json()
    articles = response.get("articles", [])
    return [{"title": a["title"], "url": a["url"]} for a in articles[:3]]
