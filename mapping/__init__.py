import copy
from typing import List

from PIL import Image

from constants import (
    STONE_FLOOR_TILE,
    WOOD_FLOOR_TILE,
    PAVING,
    DEFAULT_OBJECT,
    STONE_DOME_ROOF,
)
from validation import ImageTooBigError
from model import NMSObject


# For now, use hard-coded RGB color values. Need to find a better way to map colors to objects
MARIO_BLUE_BACKGROUND = (146, 144, 255, 255)
MARIO_RED = (181, 49, 32, 255)
MARIO_BROWN = (107, 109, 0, 255)
MARIO_FACE = (234, 158, 34, 255)
BLACK = (0, 0, 0, 0)
BLACK2 = (0, 0, 0, 255)
MM_BLUE = (0, 112, 236, 255)
MM_TEAL = (0, 232, 216, 255)
MM_FACE = (252, 216, 168, 255)
MM_WHITE = (255, 255, 255, 0)
MM_OFF_WHITE = (252, 252, 252, 255)
LINK_FACE = (252, 152, 56, 255)
LINK_BROWN = (200, 76, 12, 255)
LINK_GREEN = (128, 208, 16, 255)
LINK_GRAY = (116, 116, 116, 255)
SAM_GREEN = (0, 148, 0, 255)
SAM_ORANGE = (252, 152, 56, 255)
SAM_RED = (216, 40, 0, 255)
SAM_LIME = (184, 248, 24, 255)
SAM_WHITE = (255, 255, 255, 255)


# Oversimplified mapping of 8-bit color channel pixel colors to tuples
# Each tuple is nms_obj_type, userdata_value
# userdata seems to help determine the color of a base part in-game
color_map = {
    0: (DEFAULT_OBJECT, 0),
    MARIO_RED: (STONE_DOME_ROOF, 34),
    MARIO_BROWN: (WOOD_FLOOR_TILE, 88),
    MARIO_FACE: (STONE_FLOOR_TILE, 0),
    MARIO_BLUE_BACKGROUND: None,
    BLACK: ("^F_FLOOR", 0),
    MM_BLUE: ("^CUBEGLASS", 0),
    MM_TEAL: ("^CUBEROOM", 0),
    MM_FACE: (STONE_FLOOR_TILE, 0),
    MM_WHITE: (PAVING, 0),
    BLACK2: ("^F_FLOOR", 0),
    MM_OFF_WHITE: (PAVING, 0),
    LINK_FACE: (STONE_FLOOR_TILE, 0),
    LINK_BROWN: (WOOD_FLOOR_TILE, 88),
    LINK_GREEN: ("^T_ROOF6", 46),
    LINK_GRAY: None,
    SAM_RED: (PAVING, 4278190088),
    SAM_GREEN: (PAVING, 4278190091),
    SAM_ORANGE: (STONE_FLOOR_TILE, 0),
    # GREEN PAVER WITH "RUST" APPLIED
    SAM_LIME: (PAVING, 16777227),
    SAM_WHITE: (PAVING, 0),
}


def sprite_data_to_objects(
    sprite_data_file: str, base_computer: NMSObject, z_up=0.0
) -> List[NMSObject]:
    """Iterates through the sprite data and build an list of NMSObjects that will
    represent each pixel of the sprite."""
    result = []
    with Image.open(sprite_data_file) as image:
        # image.verify()
        pixels = list(image.getdata())
        width, height = image.size
        if width * height > MAX_BASE_OBJS:
            print("Image too big!")
            raise ImageTooBigError

        # break data into rows
        offset = 0
        TILE_DELTA = 5
        for i in pixels:
            # set x and y appropriately
            y = offset // width
            x = offset % width
            # If pixel is transparent, skip
            if i[3] != 0:
                obj_type = color_map[i]
                print(f"offset: {offset} ({x},{y})")
                tile_x = base_computer.position[0] + x * TILE_DELTA
                tile_y = base_computer.position[1] + y * TILE_DELTA
                # z is constant, flat
                tile_z = base_computer.position[2] + z_up
                print(f"Tile coord: ({tile_x}, {tile_y}, {tile_z})")
                if obj_type:
                    this_obj = create_obj_for_color(
                        base_computer, [tile_x, tile_z, tile_y], obj_type
                    )
                    result.append(this_obj)
            offset += 1
    return result


def create_obj_for_color(
    reference_object: NMSObject, offsets: List[float], obj_type: tuple[str, int]
):
    this_obj = copy.copy(reference_object)
    this_obj.at = reference_object.at
    this_obj.up = reference_object.up
    this_obj.object_id = obj_type[0]
    this_obj.timestamp = reference_object.timestamp
    this_obj.userdata = obj_type[1]
    this_obj.message = reference_object.message
    this_obj.position = [
        reference_object.position[0] + offsets[0],
        reference_object.position[1] + offsets[1],
        reference_object.position[2] + offsets[2],
    ]
    return this_obj
