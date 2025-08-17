from palette import load_nes_palette
from PIL import Image


def quantize_and_show(image_path):
    """
    Converts the specified image to the NES color palette and displays it for troubleshooting
    """
    test_image = Image.open(image_path)
    nes_palette = load_nes_palette()
    test_image_nes = test_image.convert("RGB").quantize(palette=nes_palette)
    test_image_nes.show()


quantize_and_show("sprites/picard.png")
