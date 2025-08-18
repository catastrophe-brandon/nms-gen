from PIL import Image
from mapping import build_transparency_mask
import pytest


def predict_alpha_result(image: Image):
    width, height = image.size
    image_data = image.getdata()
    alpha_pixel_count = 0
    for i in range(len(image_data)):
        y = i // width
        x = i % width
        # Assuming this is RGBA
        alpha = image.getpixel((x, y))[3]
        if alpha == 0:
            alpha_pixel_count += 1
    return alpha_pixel_count


def test_build_transparency_mask():
    test_image = Image.open("sprites/samus_standing.png")
    alpha_mask = build_transparency_mask(test_image)
    alpha_pixels = sum(alpha_mask)
    x, y = test_image.size
    assert len(alpha_mask) == x * y
    assert alpha_pixels == predict_alpha_result(test_image)

    # no alpha
    test_image = Image.open("sprites/MarioSmallFrame1.png")
    alpha_mask = build_transparency_mask(test_image)
    alpha_pixels = sum(alpha_mask)
    assert predict_alpha_result(test_image) == 0
    assert alpha_pixels == 0

    # alpha
    test_image = Image.open("sprites/mega_man_standing.png")
    x, y = test_image.size
    alpha_mask = build_transparency_mask(test_image)
    assert alpha_mask[0]
    assert len(alpha_mask) == x * y
    alpha_pixels = sum(alpha_mask)
    assert predict_alpha_result(test_image) > 0
    assert alpha_pixels > 0


def test_build_transparency_mask_with_non_rgba_image():
    test_image = Image.open("sprites/samus_standing.png")
    rgb_test_image = test_image.convert("RGB")
    with pytest.raises(ValueError):
        build_transparency_mask(rgb_test_image)
