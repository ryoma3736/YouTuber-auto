"""
AI Script Generator Module
Generates dialogue scripts from news summaries
"""
import anthropic
from config import config
from .prompts import get_prompt

class ScriptGenerator:
    """Dialogue script generator using Claude AI"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    def generate_script(self, news_summary: str) -> str:
        """
        Generate dialogue script from news summary
        Args:
            news_summary: News summary markdown
        Returns: Dialogue script
        """
        prompt_template = get_prompt('script')
        prompt = f"{prompt_template}\n\n## ニュース要約:\n{news_summary}"

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def parse_script(self, script: str) -> list[dict]:
        """
        Parse script into structured format
        Returns: List of {speaker, text} dicts
        """
        lines = script.strip().split('\n')
        parsed = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if ':' in line:
                speaker, text = line.split(':', 1)
                parsed.append({
                    'speaker': speaker.strip(),
                    'text': text.strip()
                })

        return parsed
