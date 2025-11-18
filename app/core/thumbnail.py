"""
Thumbnail Generator Module
Creates attractive YouTube thumbnails
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import tempfile


class ThumbnailGenerator:
    """YouTube thumbnail generator"""

    def __init__(self, width: int = 1280, height: int = 720):
        self.width = width
        self.height = height

    def create_thumbnail(
        self,
        title: str,
        background_color: tuple = (30, 30, 50),
        text_color: tuple = (255, 255, 255),
        output_file: str = "thumbnail.jpg"
    ) -> str:
        """
        Create simple text thumbnail
        Args:
            title: Thumbnail text
            background_color: RGB background color
            text_color: RGB text color
            output_file: Output file path
        Returns: Path to thumbnail image
        """
        print(f"🖼️  Creating thumbnail: {title}")

        # Create image
        img = Image.new('RGB', (self.width, self.height), background_color)
        draw = ImageDraw.Draw(img)

        # Try to load font
        try:
            # Try to use a Japanese font if available
            font_paths = [
                "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",  # macOS
                "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",  # Linux
                "C:\\Windows\\Fonts\\msgothic.ttc",  # Windows
            ]

            font = None
            for font_path in font_paths:
                if Path(font_path).exists():
                    font = ImageFont.truetype(font_path, 60)
                    break

            if font is None:
                # Fallback to default font
                font = ImageFont.load_default()
        except Exception as e:
            print(f"⚠️  Font loading failed: {e}, using default")
            font = ImageFont.load_default()

        # Word wrap title
        wrapped_text = self._wrap_text(title, font, self.width - 100)

        # Calculate text position (centered)
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (self.width - text_width) / 2
        y = (self.height - text_height) / 2

        # Draw text with shadow for better readability
        shadow_offset = 3
        draw.multiline_text(
            (x + shadow_offset, y + shadow_offset),
            wrapped_text,
            font=font,
            fill=(0, 0, 0),
            align='center'
        )
        draw.multiline_text(
            (x, y),
            wrapped_text,
            font=font,
            fill=text_color,
            align='center'
        )

        # Add decorative elements (optional)
        # self._add_decorations(draw)

        # Save image
        img.save(output_file, 'JPEG', quality=95)
        print(f"✅ Thumbnail saved: {output_file}")

        return output_file

    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> str:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            # Try to get text width
            try:
                bbox = font.getbbox(test_line)
                width = bbox[2] - bbox[0]
            except:
                # Fallback for default font
                width = len(test_line) * 10

            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)

    def _add_decorations(self, draw: ImageDraw):
        """Add decorative elements to thumbnail"""
        # Add corner accents
        accent_color = (255, 200, 0)
        accent_width = 10
        accent_length = 100

        # Top-left
        draw.rectangle([0, 0, accent_length, accent_width], fill=accent_color)
        draw.rectangle([0, 0, accent_width, accent_length], fill=accent_color)

        # Top-right
        draw.rectangle([self.width - accent_length, 0, self.width, accent_width], fill=accent_color)
        draw.rectangle([self.width - accent_width, 0, self.width, accent_length], fill=accent_color)

        # Bottom-left
        draw.rectangle([0, self.height - accent_width, accent_length, self.height], fill=accent_color)
        draw.rectangle([0, self.height - accent_length, accent_width, self.height], fill=accent_color)

        # Bottom-right
        draw.rectangle([self.width - accent_length, self.height - accent_width, self.width, self.height], fill=accent_color)
        draw.rectangle([self.width - accent_width, self.height - accent_length, self.width, self.height], fill=accent_color)
