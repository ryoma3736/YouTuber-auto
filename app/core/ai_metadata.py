"""
AI Metadata Generator Module
Generates YouTube title, description, and tags
"""
import anthropic
from config import config
from .prompts import get_prompt

class MetadataGenerator:
    """YouTube metadata generator using Claude AI"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    def generate_metadata(self, script: str) -> dict:
        """
        Generate YouTube metadata from script
        Args:
            script: Video script
        Returns: dict with title, description, tags
        """
        prompt_template = get_prompt('metadata')
        prompt = f"{prompt_template}\n\n## 台本:\n{script[:2000]}..."  # Limit length

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        raw_metadata = message.content[0].text

        return self._parse_metadata(raw_metadata)

    def _parse_metadata(self, raw_text: str) -> dict:
        """Parse metadata response into structured dict"""
        lines = raw_text.strip().split('\n')

        metadata = {
            'title': '',
            'description': '',
            'tags': []
        }

        current_section = None
        description_lines = []

        for line in lines:
            line = line.strip()

            if 'タイトル' in line or 'title' in line.lower():
                current_section = 'title'
                # Extract title after colon if present
                if ':' in line:
                    metadata['title'] = line.split(':', 1)[1].strip()
            elif '説明' in line or 'description' in line.lower():
                current_section = 'description'
            elif 'タグ' in line or 'tag' in line.lower():
                current_section = 'tags'
                # Extract tags after colon if present
                if ':' in line:
                    tags_str = line.split(':', 1)[1].strip()
                    metadata['tags'] = [t.strip() for t in tags_str.split(',')]
            elif current_section == 'title' and line and not metadata['title']:
                metadata['title'] = line
            elif current_section == 'description' and line:
                description_lines.append(line)
            elif current_section == 'tags' and line:
                metadata['tags'] = [t.strip() for t in line.split(',')]

        if description_lines:
            metadata['description'] = '\n'.join(description_lines)

        return metadata
