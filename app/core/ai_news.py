"""
AI News Module
Uses Claude API to search and summarize economic news
"""
import anthropic
from config import config
from .prompts import get_prompt

class NewsSearcher:
    """Economic news searcher using Claude AI"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    def search_news(self) -> str:
        """
        Search for today's important economic news
        Returns: News summary as markdown string
        """
        prompt = get_prompt('news_search')

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def get_news_summary(self) -> dict:
        """
        Get structured news summary
        Returns: dict with news items
        """
        raw_news = self.search_news()

        return {
            "raw": raw_news,
            "timestamp": None,  # TODO: Add timestamp
            "source": "Claude AI"
        }
