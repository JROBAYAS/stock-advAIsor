import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_company_news(ticker, company_name):
    """
    ticker: str, ejemplo 'AAPL'
    company_name: str, ejemplo 'Apple'
    """
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={company_name}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error NewsAPI: {response.status_code} - {response.text}")
        return []

    articles = response.json().get("articles", [])
    if not articles:
        print(f"Noticias para {company_name}: 0 artículos")
        return []

    return [{"title": a["title"], "url": a["url"]} for a in articles[:5]]