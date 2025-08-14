from PIL import Image


def load_color_palette() -> Image.Image:
    """Loads a 256 color palette from a png file."""
    return Image.open("sprites/palette.png")


def load_nes_palette() -> Image.Image:
    """Loads a 64 color palette from a png file."""
    return Image.open("sprites/NES_Palette_NTSC.png")
