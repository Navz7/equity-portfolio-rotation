import json
from datetime import datetime
import requests
import os
import csv
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(query, page=1, page_size=100):
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "pageSize": page_size,
        "page": page,
        "apiKey": API_KEY,
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Error fetching news: {response.status_code}")
        return []

    data = response.json()
    return data.get("articles", [])
#url = f'https://newsapi.org/v2/everything?q=finance+AND+(india+OR+%22indian+market%22)&country=in&pageSize=100&apiKey={API_KEY}'



def save_articles(articles, query_tag, save_as_csv=False):
    from datetime import datetime
    import json, csv

    save_dir = "data/raw_news"
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if save_as_csv:
        filename = f"{save_dir}/{query_tag}_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['source', 'author', 'title', 'description', 'url', 'publishedAt', 'content'])
            writer.writeheader()
            for article in articles:
                writer.writerow({
                    'source': article.get('source', {}).get('name'),
                    'author': article.get('author'),
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'url': article.get('url'),
                    'publishedAt': article.get('publishedAt'),
                    'content': article.get('content')
                })
    else:
        filename = f"{save_dir}/{query_tag}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)

    print(f"Successfully Saved {len(articles)} articles to {filename}")

if __name__ == "__main__":
    # Example queries — you can later loop through a list of these
    queries = {
    "overall": '(stock performance OR sector growth OR stock market trends) AND (india OR "indian market") AND ("Q2 2025" OR "quarterly results" OR "sector performance")',

    "banking": '("banking sector" OR "financial sector" OR "NBFC") AND india AND ("Q2 2025" OR "quarterly results")',

    "it": '("IT sector" OR "tech stocks" OR "software services" OR "information technology") AND india AND ("Q2 2025" OR "quarterly earnings")',

    "pharma": '("pharma sector" OR "pharmaceuticals" OR "healthcare stocks") AND india AND ("Q2 2025" OR "quarterly results")',

    "fmcg": '("FMCG" OR "consumer goods" OR "fast moving consumer goods") AND india AND ("Q2 2025" OR "demand trends" OR "sector outlook")',

    "auto": '("automobile sector" OR "auto industry" OR "EV market" OR "vehicle sales") AND india AND ("Q2 2025" OR "auto sales")',

    "energy": '("energy sector" OR "oil and gas" OR "renewable energy" OR "power sector") AND india AND ("Q2 2025" OR "energy outlook")',

    "real_estate": '("real estate sector" OR "property market" OR "housing demand") AND india AND ("Q2 2025" OR "market forecast")',

    "infrastructure": '("infrastructure" OR "construction sector" OR "capital goods") AND india AND ("Q2 2025" OR "government spending")',

    "metals": '("metal stocks" OR "steel industry" OR "mining sector") AND india AND ("Q2 2025" OR "commodity prices")',

    "telecom": '("telecom sector" OR "5G rollout" OR "telecom stocks") AND india AND ("Q2 2025" OR "subscriber growth")',

    "agriculture": '("agriculture sector" OR "agribusiness" OR "crop output" OR "rural economy") AND india AND ("Q2 2025" OR "monsoon forecast")',
    }

    for tag, q in queries.items():
        print(f"\nFetching articles for: {tag}")
        articles = fetch_news(q)
        save_articles(articles, tag)
