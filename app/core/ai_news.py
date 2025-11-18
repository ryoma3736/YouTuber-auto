"""
AI News Module
Uses Google News RSS + Claude API to fetch and summarize economic news
"""
import anthropic
from datetime import datetime
from config import config
from .prompts import get_prompt
from .news_fetcher import GoogleNewsRSSFetcher


class NewsSearcher:
    """Economic news searcher using Google News RSS + Claude AI"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.news_fetcher = GoogleNewsRSSFetcher()

    def search_news(self) -> str:
        """
        Fetch real-time news from Google News RSS and summarize with Claude
        Returns: News summary as markdown string
        """
        # Step 1: Fetch real news from Google News RSS
        print("📰 Fetching news from Google News RSS...")
        all_news = self.news_fetcher.fetch_all_economies()

        # Step 2: Format news for Claude
        news_data = self.news_fetcher.format_for_claude(all_news)

        # Step 3: Get Claude to analyze and summarize
        prompt = get_prompt('news_search')
        full_prompt = f"{prompt}\n\n{news_data}\n\n上記のニュースから、最も重要なものを各経済圏2件ずつ選び、要約してください。"

        print("🤖 Claude analyzing news...")
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=3000,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )

        return message.content[0].text

    def get_news_summary(self) -> dict:
        """
        Get structured news summary from Google News + Claude
        Returns: dict with news items
        """
        raw_news = self.search_news()

        return {
            "raw": raw_news,
            "timestamp": datetime.now().isoformat(),
            "source": "Google News RSS + Claude AI"
        }
