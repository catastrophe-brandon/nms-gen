import dataclasses
import os
import json
from pathlib import Path
from typing import List

from PIL import Image

import argparse

parser = argparse.ArgumentParser(description="Produces updated NMS base json1")
parser.add_argument(
    "base_json", type=str, help="Path to the json file containing base data"
)
parser.add_argument(
    "sprite_file", type=str, help="Path to the json file with the input sprite data"
)


def load_base_json(file_path) -> dict:
    """Loads the base data JSON"""
    with open(file_path, "r") as json_data:
        return json.load(json_data)


class InvalidBaseDataError(Exception):
    pass


class CorruptedBaseDataError(Exception):
    pass


@dataclasses.dataclass
class NMSObject(object):
    object_id = ""
    position = []
    up = []
    at = []
    timestamp = 0
    userdata = 0
    message = ""

    def __init__(self, obj_from_json_data: dict):
        self.up = obj_from_json_data.get("Up", [])
        self.timestamp = obj_from_json_data.get("Timestamp", "")
        self.at = obj_from_json_data.get("At", [])
        self.userdata = obj_from_json_data.get("UserData", 0)
        self.message = obj_from_json_data.get("Message", "")
        self.position = obj_from_json_data.get("Position", [])

    def get_z(self):
        return self.position[2]


# Object IDs of various base parts
BASE_FLAG_ID = "^BASE_FLAG"
STONE_DOME_ROOF = "^S_ROOF5"
WOOD_FLOOR_TILE = "^T_FLOOR"
STONE_FLOOR_TILE = "^S_FLOOR"
DEFAULT_OBJECT = STONE_FLOOR_TILE


def validate_base_input_data(base_input_data: dict):
    """Performs some basic checks to make sure the input JSON is valid"""
    if base_input_data.get("Objects", None) is None:
        print("Objects array in base data was not found")
        raise InvalidBaseDataError

    # Base computer should be the first object in the array
    if base_input_data.get("Objects")[0].get("ObjectID") != BASE_FLAG_ID:
        print("First object was not the base computer")
        raise InvalidBaseDataError


# For now, use hard-coded color values. Need to find a better way to map colors to objects
MARIO_BLUE_BACKGROUND = (146, 144, 255, 255)
MARIO_RED = (181, 49, 32, 255)
MARIO_BROWN = (107, 109, 0, 255)
MARIO_FACE = (234, 158, 34, 255)

# Oversimplified mapping of 8-bit color channel pixel colors to NMS object types
color_map = {
    0: DEFAULT_OBJECT,
    MARIO_RED: STONE_DOME_ROOF,
    MARIO_BROWN: WOOD_FLOOR_TILE,
    MARIO_FACE: STONE_FLOOR_TILE,
    MARIO_BLUE_BACKGROUND: None
}


def create_obj_for_color(base_computer: NMSObject, offsets: List[float], obj_type: str):
    this_obj = NMSObject(dataclasses.asdict(base_computer))
    this_obj.object_id = obj_type
    this_obj.position = [
        base_computer.position[0] + offsets[0],
        base_computer.position[1] + offsets[1],
        base_computer.position[2] + offsets[2],
    ]
    return this_obj


MAX_BASE_OBJS = 3000


class ImageTooBigError(Exception):
    pass


def sprite_data_to_objects(
        sprite_data_file:str, base_computer: NMSObject
) -> List[NMSObject]:
    result = []
    with Image.open(sprite_data_file) as image:
        # image.verify()
        pixels = list(image.getdata())
        width, height = image.size
        if width * height > MAX_BASE_OBJS:
            print("Image too big!")
            raise ImageTooBigError

        # x_start = base_computer.position[0]
        # y_start = base_computer.position[1]
        # break data into rows
        offset = 0
        for i in pixels:
            y = offset // width
            x = offset % width
            obj_type = color_map[i]
            print(f"offset: {offset} ({x},{y})")
            if obj_type:
                this_obj = create_obj_for_color(base_computer, [x, y, base_computer.position[2]], obj_type)
                result.append(this_obj)
            offset += 1
    return result


def file_exists(file_path):
    if not Path(file_path).is_file():
        print(f"The file specified does not exist: {file_path}")
        exit(1)

import dataclasses, json

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)



if __name__ == "__main__":

    args = vars(parser.parse_args())

    # path to base data json file
    base_data_file = args["base_json"]
    # path to sprite data file
    sprite_data_file = args["sprite_file"]

    file_exists(base_data_file)
    file_exists(sprite_data_file)

    try:
        base_data = load_base_json(base_data_file)
    except Exception as e:
        print(
            f"An error occurred when trying to load base json data from {base_data_file}"
        )
        print(e)
        exit(1)

    validate_base_input_data(base_data)

    base_computer = NMSObject(base_data.get("Objects")[0])

    objects = sprite_data_to_objects(sprite_data_file, base_computer)

    assert len(objects) <= MAX_BASE_OBJS

    base_data.get("Objects").extend(objects)

    print("Here comes the updated NMS base json")
    print("-=-=" * 10)
    print(json.dumps(base_data, cls=EnhancedJSONEncoder))
