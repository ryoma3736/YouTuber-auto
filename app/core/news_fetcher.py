"""
Google News RSS Fetcher
Fetches real-time news from Google News RSS feeds
"""
import feedparser
import requests
from datetime import datetime
from typing import List, Dict


class GoogleNewsRSSFetcher:
    """Fetch news from Google News RSS"""

    def __init__(self):
        self.base_url = "https://news.google.com/rss"

    def fetch_japan_news(self, max_results: int = 5) -> List[Dict]:
        """
        Fetch Japanese economic news
        Returns: List of news items
        """
        # Google News RSS for Japan Business news
        url = f"{self.base_url}/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtcGhHZ0pLVUNnQVAB?hl=ja&gl=JP&ceid=JP:ja"

        return self._fetch_feed(url, max_results, "日本")

    def fetch_us_news(self, max_results: int = 5) -> List[Dict]:
        """
        Fetch US economic news
        Returns: List of news items
        """
        # Google News RSS for US Business news
        url = f"{self.base_url}/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en"

        return self._fetch_feed(url, max_results, "米国")

    def fetch_china_news(self, max_results: int = 5) -> List[Dict]:
        """
        Fetch China economic news
        Returns: List of news items
        """
        # Google News RSS for China Business news (in English or Japanese)
        # Using search query for China economic news
        import urllib.parse
        query = "中国経済"
        encoded_query = urllib.parse.quote(query)
        url = f"{self.base_url}/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"

        return self._fetch_feed(url, max_results, "中国")

    def _fetch_feed(self, url: str, max_results: int, region: str) -> List[Dict]:
        """
        Fetch and parse RSS feed
        Args:
            url: RSS feed URL
            max_results: Maximum number of results
            region: Region name (for logging)
        Returns: List of parsed news items
        """
        try:
            print(f"📰 Fetching {region} news from Google News RSS...")

            # Parse RSS feed
            feed = feedparser.parse(url)

            news_items = []
            for entry in feed.entries[:max_results]:
                item = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', ''),
                    'source': entry.get('source', {}).get('title', 'Google News'),
                    'region': region
                }
                news_items.append(item)

            print(f"✅ Found {len(news_items)} {region} news items")
            return news_items

        except Exception as e:
            print(f"❌ Error fetching {region} news: {e}")
            return []

    def fetch_all_economies(self) -> Dict[str, List[Dict]]:
        """
        Fetch news from all 3 major economies
        Returns: Dict with news for Japan, US, China
        """
        return {
            'japan': self.fetch_japan_news(max_results=3),
            'us': self.fetch_us_news(max_results=3),
            'china': self.fetch_china_news(max_results=3)
        }

    def format_for_claude(self, all_news: Dict[str, List[Dict]]) -> str:
        """
        Format fetched news for Claude AI processing
        Args:
            all_news: Dict with news from all regions
        Returns: Formatted string for Claude
        """
        formatted = "# 本日の経済ニュース（Google News RSS）\n\n"

        # Japan
        formatted += "## 🇯🇵 日本経済ニュース\n"
        for idx, item in enumerate(all_news.get('japan', []), 1):
            formatted += f"\n### {idx}. {item['title']}\n"
            formatted += f"- ソース: {item['source']}\n"
            formatted += f"- 公開: {item['published']}\n"
            formatted += f"- URL: {item['link']}\n"
            if item['summary']:
                formatted += f"- 概要: {item['summary']}\n"

        # US
        formatted += "\n## 🇺🇸 米国経済ニュース\n"
        for idx, item in enumerate(all_news.get('us', []), 1):
            formatted += f"\n### {idx}. {item['title']}\n"
            formatted += f"- ソース: {item['source']}\n"
            formatted += f"- 公開: {item['published']}\n"
            formatted += f"- URL: {item['link']}\n"
            if item['summary']:
                formatted += f"- 概要: {item['summary']}\n"

        # China
        formatted += "\n## 🇨🇳 中国経済ニュース\n"
        for idx, item in enumerate(all_news.get('china', []), 1):
            formatted += f"\n### {idx}. {item['title']}\n"
            formatted += f"- ソース: {item['source']}\n"
            formatted += f"- 公開: {item['published']}\n"
            formatted += f"- URL: {item['link']}\n"
            if item['summary']:
                formatted += f"- 概要: {item['summary']}\n"

        return formatted
