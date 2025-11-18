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


class VideoPipeline:
    """Main video generation pipeline"""

    def __init__(self, user_id: str = None):
        self.user_id = user_id
        self.notifier = LineNotifier() if user_id else None

        # Initialize all modules
        self.news_searcher = NewsSearcher()
        self.script_generator = ScriptGenerator()
        self.metadata_generator = MetadataGenerator()

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

            # Step 4: TTS (TODO: Implement)
            print("\n🎤 Audio generation (not implemented yet)")

            # Step 5: Video generation (TODO: Implement)
            print("\n🎬 Video generation (not implemented yet)")

            # Step 6: YouTube upload (TODO: Implement)
            print("\n📤 YouTube upload (not implemented yet)")

            result = {
                'status': 'success',
                'news': news_summary,
                'script': script,
                'metadata': metadata
            }

            if self.notifier:
                self.notifier.notify_success(
                    self.user_id,
                    metadata['title'],
                    "https://youtube.com/watch?v=dummy"  # Placeholder
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
