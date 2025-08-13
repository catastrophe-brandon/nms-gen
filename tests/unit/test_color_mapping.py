from PIL import Image

from palette import load_color_palette


def test_color_palette_quantization():
    """Ensure that two images quantized from the same palette actually use the same colors"""
    palette = load_color_palette()
    mario = Image.open("./sprites/MarioSmallFrame1.png")
    link = Image.open("./sprites/link_sprite.png")
    mario_q = mario.convert("RGB").quantize(colors=256, palette=palette)
    link_q = link.convert("RGB").quantize(colors=256, palette=palette)

    assert len(mario_q.palette.colors) == 256
    assert len(link_q.palette.colors) == 256
    assert link_q.palette.colors == mario_q.palette.colors

    # link's face and mario's face are different colors in RGB
    assert mario_q.getpixel((2, 7)) != link_q.getpixel((2, 2))


def test_two_images_same_palette():
    palette = load_color_palette()
    samus1 = Image.open("./sprites/samus_facing.png")
    samus2 = Image.open("./sprites/samus_standing.png")
    samus1_q = samus1.convert("RGB").quantize(colors=256, palette=palette)
    samus2_q = samus2.convert("RGB").quantize(colors=256, palette=palette)
    assert samus1_q.palette.colors == samus2_q.palette.colors
