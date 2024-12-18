import io
import pytesseract
from PIL import Image, ImageEnhance
from django import forms
from django.core.exceptions import ValidationError


class ImageTextExtractionForm(forms.Form):
    image = forms.ImageField(
        label="Upload Image",
        help_text="Supported formats: PNG, JPG, JPEG, GIF, BMP, WebP",
    )

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image.size > 5 * 1024 * 1024:
            raise ValidationError("Image file too large. Maximum size is 5MB.")

        allowed_types = [
            "image/png",
            "image/jpeg",
            "image/gif",
            "image/bmp",
            "image/webp",
        ]
        if image.content_type not in allowed_types:
            raise ValidationError("Unsupported image format.")

        return image

    def extract_text(self):
        image = self.cleaned_data.get("image")

        if not image:
            return None

        try:
            img = Image.open(io.BytesIO(image.read()))
            img = img.convert("L")
            img = ImageEnhance.Contrast(img).enhance(2)
            img = img.resize((img.width * 2, img.height * 2))

            extracted_text = pytesseract.image_to_string(
                img, lang="kaz+rus+eng", config="--oem 3 --psm 6"
            ).strip()

            text = clean_whitespace(extracted_text)

            return text

        except Exception as e:
            return f"Error: {e}"

    def save(self, *args, **kwargs):
        return self.extract_text()


def clean_whitespace(text):
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())
