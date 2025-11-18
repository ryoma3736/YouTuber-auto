"""
Main Pipeline Runner
Orchestrates the entire video generation process
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.core.ai_news import NewsSearcher
from app.core.ai_script import ScriptGenerator
from app.core.ai_metadata import MetadataGenerator
from app.core.line_notify import LineNotifier
from app.core.tts import GeminiTTS
from app.core.video import VideoGenerator
from app.core.thumbnail import ThumbnailGenerator
from app.core.youtube_uploader import YouTubeUploader


class VideoPipeline:
    """Main video generation pipeline"""

    def __init__(self, user_id: str = None, enable_full_pipeline: bool = False):
        self.user_id = user_id
        self.notifier = LineNotifier() if user_id else None
        self.enable_full_pipeline = enable_full_pipeline

        # Initialize all modules
        self.news_searcher = NewsSearcher()
        self.script_generator = ScriptGenerator()
        self.metadata_generator = MetadataGenerator()

        # Initialize media modules (only if full pipeline enabled)
        if enable_full_pipeline:
            self.tts = GeminiTTS()
            self.video_gen = VideoGenerator()
            self.thumbnail_gen = ThumbnailGenerator()
            self.youtube_uploader = YouTubeUploader()

    def run(self) -> dict:
        """
        Execute full pipeline
        Returns: dict with results
        """
        try:
            if self.notifier:
                self.notifier.notify_start(self.user_id)

            # Step 1: Search news
            print("📰 Searching for economic news...")
            news_result = self.news_searcher.get_news_summary()
            news_summary = news_result['raw']
            print(f"✅ Found news:\n{news_summary[:200]}...")

            # Step 2: Generate script
            print("\n📝 Generating dialogue script...")
            script = self.script_generator.generate_script(news_summary)
            parsed_script = self.script_generator.parse_script(script)
            print(f"✅ Generated script with {len(parsed_script)} dialogue lines")

            # Step 3: Generate metadata
            print("\n🏷️  Generating metadata...")
            metadata = self.metadata_generator.generate_metadata(script)
            print(f"✅ Title: {metadata['title']}")

            # Step 4: TTS
            audio_file = None
            if self.enable_full_pipeline:
                print("\n🎤 Generating audio...")
                audio_files = self.tts.generate_audio(parsed_script, output_dir="temp/audio")
                audio_file = self.tts.concatenate_audio(audio_files, "temp/final_audio.wav")
                print(f"✅ Audio generated: {audio_file}")
            else:
                print("\n🎤 Audio generation (skipped - demo mode)")

            # Step 5: Video generation
            video_file = None
            if self.enable_full_pipeline and audio_file:
                print("\n🎬 Generating video...")
                video_file = self.video_gen.create_video(
                    audio_file=audio_file,
                    output_file="temp/final_video.mp4"
                )
                print(f"✅ Video generated: {video_file}")
            else:
                print("\n🎬 Video generation (skipped - demo mode)")

            # Step 6: Generate thumbnail
            thumbnail_file = None
            if self.enable_full_pipeline:
                print("\n🖼️  Generating thumbnail...")
                thumbnail_file = self.thumbnail_gen.create_thumbnail(
                    title=metadata['title'],
                    output_file="temp/thumbnail.jpg"
                )
                print(f"✅ Thumbnail generated: {thumbnail_file}")
            else:
                print("\n🖼️  Thumbnail generation (skipped - demo mode)")

            # Step 7: YouTube upload
            youtube_url = None
            if self.enable_full_pipeline and video_file:
                print("\n📤 Uploading to YouTube...")
                upload_result = self.youtube_uploader.upload_video(
                    video_file=video_file,
                    title=metadata['title'],
                    description=metadata['description'],
                    tags=metadata['tags'],
                    thumbnail_file=thumbnail_file
                )
                youtube_url = upload_result['url']
                print(f"✅ Uploaded: {youtube_url}")
            else:
                print("\n📤 YouTube upload (skipped - demo mode)")
                youtube_url = "https://youtube.com/watch?v=demo"

            result = {
                'status': 'success',
                'news': news_summary,
                'script': script,
                'metadata': metadata,
                'audio_file': audio_file,
                'video_file': video_file,
                'thumbnail_file': thumbnail_file,
                'youtube_url': youtube_url
            }

            if self.notifier:
                self.notifier.notify_success(
                    self.user_id,
                    metadata['title'],
                    youtube_url
                )

            return result

        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")
            if self.notifier:
                self.notifier.notify_error(self.user_id, "Pipeline", str(e))
            raise


def main():
    """CLI entry point"""
    print("🚀 Starting YouTube Video Generation Pipeline\n")
    pipeline = VideoPipeline()
    result = pipeline.run()
    print("\n✅ Pipeline completed successfully!")
    print(f"Title: {result['metadata']['title']}")


if __name__ == "__main__":
    main()
