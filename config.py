"""
Configuration management for YouTube Auto Generator
Loads environment variables and provides configuration access
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""

    # API Keys
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')

    # LINE Integration
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')

    # YouTube API
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID', '')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET', '')
    YOUTUBE_REFRESH_TOKEN = os.getenv('YOUTUBE_REFRESH_TOKEN', '')

    # Google Drive
    GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '')

    # Server
    PORT = int(os.getenv('PORT', '8000'))
    HOST = os.getenv('HOST', '0.0.0.0')

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = [
            'ANTHROPIC_API_KEY',
            'GEMINI_API_KEY',
            'LINE_CHANNEL_SECRET',
            'LINE_CHANNEL_ACCESS_TOKEN'
        ]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        return True

config = Config()
