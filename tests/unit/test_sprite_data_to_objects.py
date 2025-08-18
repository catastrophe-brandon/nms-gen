from PIL import Image
import pytest
from PIL.Image import Dither
from mapping import sprite_data_to_objects, build_transparency_mask
from model import NMSObject
from palette import load_nes_palette
from validation import InvalidImageType

default_anchor = NMSObject(
    {
        "Up": [0, 0, 0],
        "At": [0, 0, 0],
        "UserData": 0,
        "Message": "",
        "Position": [0, 0, 0],
    }
)


def test_sprite_data_to_objects_with_nes_palette():
    test_image = Image.open("sprites/test_image_nes.png")
    test_image = test_image.convert("RGB").quantize(colors=64, dither=Dither.NONE)
    nms_objects = sprite_data_to_objects(test_image, anchor_object=default_anchor)
    assert len(nms_objects) == 64


def test_sprite_data_to_objects_without_nes_palette():
    test_image = Image.open("sprites/test_image_nes.png")
    with pytest.raises(InvalidImageType):
        sprite_data_to_objects(test_image, anchor_object=default_anchor)


def test_mario_to_objects():
    test_image = Image.open("sprites/MarioSmallFrame1.png")

    test_image = test_image.convert("RGB").quantize(
        colors=64, palette=load_nes_palette()
    )
    nms_objects = sprite_data_to_objects(test_image, anchor_object=default_anchor)
    assert len(nms_objects) == 16 * 16


def test_sprite_data_to_objects_with_transparency():
    test_image = Image.open("sprites/mega_man_standing.png")
    alpha_mask = build_transparency_mask(test_image)
    test_image = test_image.convert("RGB").quantize(
        colors=64, dither=Dither.NONE, palette=load_nes_palette()
    )
    nms_objects = sprite_data_to_objects(
        test_image, anchor_object=default_anchor, transparency_mask=alpha_mask
    )
    assert len(nms_objects) < test_image.size[0] * test_image.size[1]
