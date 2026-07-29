"""Provide images for BfG functions."""

import base64
import io
from pathlib import Path

from bridgeobjects import CARD_NAMES
from PIL import Image as PilImage

BASE_DIRECTORY = "locale/en_GB"
IMAGE_DIRECTORY = "images"
CARD_IMAGE_DIRECTORY = "card_images"
IMAGE_EXTENSION = "png"


class BaseImage:
    """Base class for images."""

    def __init__(self, name, source_directory, rotate):
        self.name = name
        image_directory = Path(
            Path(__file__).parent.parent,
            BASE_DIRECTORY,
            IMAGE_DIRECTORY,
            source_directory,
        )
        image_path = Path(image_directory, f"{name}.{IMAGE_EXTENSION}")
        image = PilImage.open(image_path)
        if rotate:
            image = image.rotate(90, expand=1)
        self.image = self._encode_image(image)

    @staticmethod
    def _encode_image(image):
        """Return image encoded to base64 from a PIL.Image.Image."""
        io_buffer = io.BytesIO()
        image.save(io_buffer, format="PNG")
        saved_image = io_buffer.getvalue()
        return "".join(
            ["data:image/jpg;base64,", base64.b64encode(saved_image).decode()]
        )


class CardImage(BaseImage):
    """Defines a single card image."""

    def __init__(self, name, rotate=False):
        super().__init__(name, CARD_IMAGE_DIRECTORY, rotate)

    def __repr__(self):
        return f'CardImage("{self.name}")'

    def __str__(self):
        return f"CardImage: {self.name}"

    @staticmethod
    def get_images():
        """Return a dict of call images."""
        images = {card: CardImage(card).image for card in CARD_NAMES}
        images["back"] = CardImage("back").image
        images["back_rotated"] = CardImage("back", rotate=True).image
        images["blank"] = CardImage("blank").image
        return images


# card_images is a dict that contains all the valid cards
card_images = CardImage.get_images()
