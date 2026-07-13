import requests
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()

class NewsFetcher:
    def __init__(self, api_key: str = None):
        """Initialize NewsAPI fetcher"""
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
        
        if not self.api_key:
            raise ValueError("NEWS_API_KEY not found. Set it in .env file or pass it directly.")
    
    def fetch_financial_news(self, query: str = "earnings", limit: int = 10) -> List[Dict]:
        """
        Fetch financial news articles
        
        Args:
            query: Search term (e.g., 'earnings', 'guidance', 'Apple earnings')
            limit: Number of articles to return
        
        Returns:
            List of article dictionaries with title, description, url, etc.
        """
        try:
            params = {
                'q': query,
                'apiKey': self.api_key,
                'pageSize': limit,
                'sortBy': 'publishedAt',
                'language': 'en'
            }
            
            response = requests.get(f"{self.base_url}/everything", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'ok':
                print(f"Error: {data.get('message', 'Unknown error')}")
                return []
            
            articles = []
            for article in data['articles']:
                articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'publishedAt': article.get('publishedAt', ''),
                    'content': article.get('content', '')
                })
            
            return articles
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return []
    
    def fetch_stock_news(self, ticker: str, limit: int = 10) -> List[Dict]:
        """Fetch news for a specific stock ticker"""
        return self.fetch_financial_news(query=ticker, limit=limit)
    
    def fetch_multiple_stocks(self, tickers: List[str], limit: int = 5) -> Dict[str, List[Dict]]:
        """Fetch news for multiple stock tickers"""
        results = {}
        for ticker in tickers:
            results[ticker] = self.fetch_stock_news(ticker, limit)
        return results


if __name__ == "__main__":
    # Test the fetcher
    fetcher = NewsFetcher()
    
    # Fetch earnings news
    print("Fetching earnings news...")
    articles = fetcher.fetch_financial_news("earnings", limit=5)
    
    for article in articles:
        print(f"\nTitle: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"URL: {article['url']}")
