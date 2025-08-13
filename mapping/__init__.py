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
)
from validation import ImageTooBigError
from model import NMSObject, create_from_reference_object

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

# New color map for 256 color palette mapping
# Maps color indexes to tuples with NMS Object IDs and userdata values
color_index_map = {0: (DEFAULT_OBJECT_ID, 0)}


def sprite_data_to_objects(
    image: Image, base_computer: NMSObject, z_up=0.0, tile_spacing=5
) -> List[NMSObject]:
    """Iterates through the sprite data and build a list of NMSObjects that will
    represent each pixel of the sprite. Be sure to run validation before invoking this function."""
    result = []

    pixels = list(image.getdata())
    width, height = image.size
    if width * height > MAX_BASE_OBJS:
        logger.error("Image too big!")
        raise ImageTooBigError

    # break data into rows
    offset = 0
    for i in pixels:
        # set x and y appropriately
        y = offset // width
        x = offset % width
        # If pixel is transparent, skip
        # TODO: Figure out how to handle transparency
        if i[3] != 0:
            # TODO: logging setup
            object_id = color_map[i][0]
            object_userdata = color_map[i][1]
            logger.debug(f"offset: {offset} ({x},{y})")
            tile_x = base_computer.position[0] + x * tile_spacing
            tile_y = base_computer.position[1] + y * tile_spacing
            # z is constant, flat
            tile_z = base_computer.position[2] + z_up
            logger.debug(f"Tile coord: ({tile_x}, {tile_y}, {tile_z})")
            if object_id:
                this_obj = create_from_reference_object(
                    base_computer, [tile_x, tile_z, tile_y], object_id, object_userdata
                )
                result.append(this_obj)
        offset += 1
    return result
