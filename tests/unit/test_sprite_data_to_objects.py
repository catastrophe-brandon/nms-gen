from PIL import Image
from mapping import sprite_data_to_objects
from model import NMSObject


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
