from PIL import Image
from mapping import sprite_data_to_objects
from model import NMSObject
from palette import load_nes_palette


def test_sprite_data_to_objects_with_nes_palette():
    test_image = Image.open("sprites/test_image_nes.png")

    # Note: Remember that case matters on the dict attributes
    anchor_object = NMSObject(
        {
            "Up": [0, 0, 0],
            "At": [0, 0, 0],
            "UserData": 0,
            "Message": "",
            "Position": [0, 0, 0],
        }
    )

    nms_objects = sprite_data_to_objects(test_image, anchor_object=anchor_object)
    assert len(nms_objects) == 64


def test_mario_to_objects():
    test_image = Image.open("sprites/MarioSmallFrame1.png")

    # Note: Remember that case matters on the dict attributes
    anchor_object = NMSObject(
        {
            "Up": [0, 0, 0],
            "At": [0, 0, 0],
            "UserData": 0,
            "Message": "",
            "Position": [0, 0, 0],
        }
    )
    test_image = test_image.convert("RGB").quantize(
        colors=64, palette=load_nes_palette()
    )
    nms_objects = sprite_data_to_objects(test_image, anchor_object=anchor_object)
    assert len(nms_objects) == 16 * 16
