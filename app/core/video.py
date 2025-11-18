"""
Video Generation Module
Creates video files from audio and background images using MoviePy
"""
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    TextClip,
    concatenate_videoclips
)
from pathlib import Path
import tempfile


class VideoGenerator:
    """Video generator using MoviePy"""

    def __init__(self, width: int = 1920, height: int = 1080, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps

    def create_video(
        self,
        audio_file: str,
        background_image: str = None,
        subtitles: list[dict] = None,
        output_file: str = "output.mp4"
    ) -> str:
        """
        Create video from audio and background
        Args:
            audio_file: Path to audio file
            background_image: Path to background image (optional)
            subtitles: List of {text, start, end} dicts (optional)
            output_file: Output video path
        Returns: Path to generated video
        """
        print(f"🎬 Creating video: {output_file}")

        # Load audio
        audio = AudioFileClip(audio_file)
        duration = audio.duration

        # Create or load background
        if background_image and Path(background_image).exists():
            background = ImageClip(background_image).set_duration(duration)
        else:
            # Create solid color background
            background = self._create_solid_background(duration)

        # Resize background to fit dimensions
        background = background.resize((self.width, self.height))

        # Add subtitles if provided
        if subtitles:
            subtitle_clips = self._create_subtitle_clips(subtitles)
            video = CompositeVideoClip([background] + subtitle_clips)
        else:
            video = background

        # Set audio
        video = video.set_audio(audio)

        # Write output
        video.write_videofile(
            output_file,
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )

        # Clean up
        audio.close()
        background.close()
        if subtitles:
            for clip in subtitle_clips:
                clip.close()

        print(f"✅ Video created: {output_file}")
        return output_file

    def _create_solid_background(self, duration: float, color: tuple = (30, 30, 50)) -> ImageClip:
        """Create a solid color background"""
        from PIL import Image
        import numpy as np

        # Create image
        img_array = np.full((self.height, self.width, 3), color, dtype=np.uint8)
        img = Image.fromarray(img_array)

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            img.save(f.name)
            temp_path = f.name

        # Create clip
        clip = ImageClip(temp_path).set_duration(duration)
        return clip

    def _create_subtitle_clips(self, subtitles: list[dict]) -> list[TextClip]:
        """Create subtitle text clips"""
        subtitle_clips = []

        for sub in subtitles:
            text = sub['text']
            start = sub['start']
            end = sub['end']

            # Create text clip
            txt_clip = TextClip(
                text,
                fontsize=40,
                color='white',
                bg_color='black',
                size=(self.width - 100, None),
                method='caption'
            )

            # Position at bottom center
            txt_clip = txt_clip.set_position(('center', self.height - 150))
            txt_clip = txt_clip.set_start(start).set_end(end)

            subtitle_clips.append(txt_clip)

        return subtitle_clips

    def add_bgm(self, video_file: str, bgm_file: str, bgm_volume: float = 0.1) -> str:
        """
        Add background music to video
        Args:
            video_file: Input video path
            bgm_file: Background music path
            bgm_volume: BGM volume (0.0 to 1.0)
        Returns: Path to output video
        """
        from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

        video = VideoFileClip(video_file)
        bgm = AudioFileClip(bgm_file).volumex(bgm_volume)

        # Loop BGM if shorter than video
        if bgm.duration < video.duration:
            bgm = bgm.loop(duration=video.duration)
        else:
            bgm = bgm.subclip(0, video.duration)

        # Composite audio
        if video.audio:
            final_audio = CompositeAudioClip([video.audio, bgm])
        else:
            final_audio = bgm

        video = video.set_audio(final_audio)

        # Output path
        output_file = video_file.replace('.mp4', '_with_bgm.mp4')
        video.write_videofile(output_file, codec='libx264', audio_codec='aac')

        # Clean up
        video.close()
        bgm.close()

        return output_file
