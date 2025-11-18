"""
YouTube Upload Module
Uploads videos to YouTube using YouTube Data API v3
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import config
import os


class YouTubeUploader:
    """YouTube video uploader"""

    def __init__(self):
        self.credentials = self._get_credentials()
        self.youtube = build('youtube', 'v3', credentials=self.credentials)

    def _get_credentials(self) -> Credentials:
        """Get OAuth2 credentials"""
        # For production, use refresh token
        credentials = Credentials(
            token=None,
            refresh_token=config.YOUTUBE_REFRESH_TOKEN,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=config.YOUTUBE_CLIENT_ID,
            client_secret=config.YOUTUBE_CLIENT_SECRET
        )
        return credentials

    def upload_video(
        self,
        video_file: str,
        title: str,
        description: str,
        tags: list[str] = None,
        category_id: str = '25',  # News & Politics
        privacy_status: str = 'public',
        thumbnail_file: str = None
    ) -> dict:
        """
        Upload video to YouTube
        Args:
            video_file: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID
            privacy_status: 'public', 'private', or 'unlisted'
            thumbnail_file: Path to thumbnail image (optional)
        Returns: dict with video info including video_id and url
        """
        print(f"📤 Uploading video to YouTube: {title}")

        # Prepare request body
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }

        # Create media file upload
        if not os.path.exists(video_file):
            raise FileNotFoundError(f"Video file not found: {video_file}")

        media = MediaFileUpload(
            video_file,
            chunksize=1024*1024,  # 1MB chunks
            resumable=True,
            mimetype='video/*'
        )

        # Execute upload
        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"⏳ Upload progress: {progress}%")

        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"✅ Video uploaded successfully!")
        print(f"📹 Video ID: {video_id}")
        print(f"🔗 URL: {video_url}")

        # Upload thumbnail if provided
        if thumbnail_file and os.path.exists(thumbnail_file):
            self._upload_thumbnail(video_id, thumbnail_file)

        return {
            'video_id': video_id,
            'url': video_url,
            'title': title,
            'status': 'success'
        }

    def _upload_thumbnail(self, video_id: str, thumbnail_file: str):
        """Upload custom thumbnail"""
        print(f"🖼️  Uploading thumbnail...")

        media = MediaFileUpload(thumbnail_file, mimetype='image/jpeg')

        self.youtube.thumbnails().set(
            videoId=video_id,
            media_body=media
        ).execute()

        print(f"✅ Thumbnail uploaded")

    def get_video_info(self, video_id: str) -> dict:
        """Get video information"""
        request = self.youtube.videos().list(
            part='snippet,statistics,status',
            id=video_id
        )

        response = request.execute()

        if not response['items']:
            raise ValueError(f"Video not found: {video_id}")

        return response['items'][0]

    def update_video(
        self,
        video_id: str,
        title: str = None,
        description: str = None,
        tags: list[str] = None
    ) -> dict:
        """Update video metadata"""
        # Get current video info
        current = self.get_video_info(video_id)

        # Update fields
        snippet = current['snippet']
        if title:
            snippet['title'] = title
        if description:
            snippet['description'] = description
        if tags:
            snippet['tags'] = tags

        # Execute update
        request = self.youtube.videos().update(
            part='snippet',
            body={
                'id': video_id,
                'snippet': snippet
            }
        )

        response = request.execute()
        print(f"✅ Video updated: {video_id}")

        return response
