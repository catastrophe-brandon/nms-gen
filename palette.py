from PIL import Image


def load_color_palette() -> Image.Image:
    return Image.open("sprites/palette.png")
