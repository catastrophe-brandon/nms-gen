from typing import List

from PIL import Image
import logging

logger = logging.getLogger(__name__)

from constants import (
    STONE_FLOOR_TILE,
    WOOD_FLOOR_TILE,
    PAVING,
    DEFAULT_OBJECT_ID,
    STONE_DOME_ROOF,
    MAX_BASE_OBJS,
    OLD_WOOD_FLOOR,
    CUBE_SOLID,
    WOOD_ROOF,
    METAL_FLOOR,
)
from validation import ImageTooBigError
from model import NMSObject, create_from_reference_object

# For now, use hard-coded RGB color values. Need to find a better way to map colors to objects
MARIO_BLUE_BACKGROUND = (146, 144, 255, 255)
MARIO_RED = (181, 49, 32, 255)
MARIO_BROWN = (107, 109, 0, 255)
MARIO_FACE = (234, 158, 34, 255)
BLACK = ((0, 0, 0, 0),)
BLACK2 = (0, 0, 0, 255)
MM_BLUE = (0, 112, 236, 255)
MM_TEAL = (0, 232, 216, 255)
MM_FACE = (252, 216, 168, 255)
MM_WHITE = ((255, 255, 255, 0),)
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


# Oversimplified mapping of pixel data tuples representing NMS Objects and modifiers (userdata)
# Each tuple is nms_obj_type, userdata_value
# userdata seems to help determine the color of a base part in-game
color_map = {
    0: (DEFAULT_OBJECT_ID, 0),
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

# BUILD_PAVING_BIG with 0x0 userdata modifier applied, white
WHITE_TILE = (PAVING, 0)
RED_TILE = (OLD_WOOD_FLOOR, 8)
BLACK_TILE = ("^F_FLOOR", 0)


# New color map for 64 color palette mapping
# Maps color indexes to tuples with NMS Object IDs and userdata values
color_index_map = {
    # === Row 0
    # (124, 124, 124) - Darker Gray
    0: (CUBE_SOLID, 15),
    # (188, 188, 188) - Lighter gray
    1: (CUBE_SOLID, 14),
    # (0, 120, 248) - Blue
    2: (OLD_WOOD_FLOOR, 5),
    # (0, 88, 248), 0x1000008 - Slightly lighter blue
    3: (PAVING, 5),
    # (104, 68, 252)
    4: (PAVING, 13),
    # (216, 0, 204) - 0x3000007
    5: (PAVING, 50331655),
    6: RED_TILE,
    7: (PAVING, 16777224),
    # === Row 1
    8: (OLD_WOOD_FLOOR, 10),
    9: (WOOD_FLOOR_TILE, 0),
    10: (PAVING, 33554443),
    11: (PAVING, 11),
    12: (PAVING, 11),
    13: (OLD_WOOD_FLOOR, 12),
    14: BLACK_TILE,
    15: BLACK_TILE,
    # === Row 2
    16: BLACK_TILE,
    17: (PAVING, 0),
    18: (OLD_WOOD_FLOOR, 4),
    19: (OLD_WOOD_FLOOR, 6),
    20: (OLD_WOOD_FLOOR, 6),
    21: (PAVING, 50331655),
    22: (PAVING, 16777224),
    23: (DEFAULT_OBJECT_ID, 0),
    # === Row 3
    24: (STONE_FLOOR_TILE, 27),
    25: (STONE_FLOOR_TILE, 16777241),
    26: (PAVING, 16777227),
    27: (WOOD_FLOOR_TILE, 12),
    28: (WOOD_FLOOR_TILE, 12),
    29: (PAVING, 3),
    30: (PAVING, 14),
    31: BLACK_TILE,
    # === Row 4
    32: BLACK_TILE,
    33: (PAVING, 0),
    34: (PAVING, 3),
    35: (PAVING, 16777223),
    36: (PAVING, 16777223),
    37: (PAVING, 16777223),
    38: (PAVING, 16777223),
    39: (STONE_FLOOR_TILE, 24),
    # === Row 5
    40: (STONE_FLOOR_TILE, 25),
    41: (STONE_FLOOR_TILE, 24),
    42: (STONE_FLOOR_TILE, 30),
    43: (STONE_FLOOR_TILE, 30),
    44: (STONE_FLOOR_TILE, 30),
    45: (WOOD_ROOF, 78),
    46: (PAVING, 16777223),
    47: (METAL_FLOOR, 50),
    # === Row 6
    48: BLACK_TILE,
    49: (PAVING, 50331656),
    50: (PAVING, 50331656),
    51: (PAVING, 8),
    52: (WOOD_ROOF, 16777293),
    53: (PAVING, 11),
    54: (PAVING, 50331659),
    55: (PAVING, 50331659),
    # === Row 7
    # Brighter blue
    56: (PAVING, 4),
    # Darker Blue
    57: (PAVING, 5),
    # Violet
    58: (OLD_WOOD_FLOOR, 6),
    # Darker ping
    59: (OLD_WOOD_FLOOR, 6),
    # Greenish gray?
    60: (PAVING, 50331659),
    61: BLACK_TILE,
    62: BLACK_TILE,
    63: BLACK_TILE,
}


def sprite_data_to_objects(
    image: Image, anchor_object: NMSObject, z_up=0.0, tile_spacing=5
) -> List[NMSObject]:
    """Iterates through the sprite data and build a list of NMSObjects that will
    represent each pixel of the sprite. Be sure to run validation before invoking this function."""
    result = []

    pixels = list(image.getdata())
    width, height = image.size
    # if width * height > MAX_BASE_OBJS:
    #     logger.error("Image too big!")
    #     raise ImageTooBigError

    # break data into rows
    offset = 0
    for i in range(len(pixels)):
        # set x and y appropriately
        y = offset // width
        x = offset % width
        # If pixel is transparent, skip
        # TODO: Figure out how to handle transparency
        pixel_color_index = pixels[i]
        object_id = color_index_map[pixel_color_index][0]
        object_userdata = color_index_map[pixel_color_index][1]
        logger.debug(f"offset: {offset} ({x},{y})")
        tile_x = anchor_object.position[0] + x * tile_spacing
        tile_y = anchor_object.position[1] + y * tile_spacing
        # z is constant, flat
        tile_z = anchor_object.position[2] + z_up
        logger.debug(f"Tile coord: ({tile_x}, {tile_y}, {tile_z})")
        if object_id:
            this_obj = create_from_reference_object(
                anchor_object, [tile_x, tile_z, tile_y], object_id, object_userdata
            )
            result.append(this_obj)
        offset += 1
    return result
