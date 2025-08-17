import json
from pathlib import Path

import argparse

from PIL import Image

from mapping import sprite_data_to_objects
from model import NMSObject
import logging

from palette import load_nes_palette
from validation import validate_base_input_data, validate_pixel_input_data

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description="Produces updated NMS base JSON data from PNG image data (pixel art); intended to be used with NMS Save Editor"
)
parser.add_argument(
    "base_json", type=str, help="Path to the JSON file containing base data"
)
parser.add_argument(
    "sprite_file", type=str, help="Path to the PNG file with the input sprite data"
)
parser.add_argument(
    "z_up",
    type=float,
    help="Vertical adjustment (Z) to put tiles above terrain",
    default=5.0,
)
parser.add_argument("--o", type=str, help="Path to JSON output file")


def load_base_json(file_path) -> dict:
    """Loads the base data JSON from a file"""
    with open(file_path, "r") as json_data:
        return json.load(json_data)


def file_exists(file_path):
    if not Path(file_path).is_file():
        logger.error(f"The file specified does not exist: {file_path}")
        exit(1)


if __name__ == "__main__":
    args = vars(parser.parse_args())

    # path to base data JSON file
    base_data_file = args["base_json"]

    # path to a sprite data file
    sprite_data_file = args["sprite_file"]

    output_file = args["o"]

    z_up = args["z_up"]
    logger.debug(f"z_up is {z_up}")

    file_exists(base_data_file)
    file_exists(sprite_data_file)

    try:
        base_data = load_base_json(base_data_file)
    except Exception as e:
        logger.error(
            f"An error occurred when trying to load base json data from {base_data_file}"
        )
        logger.error(e)
        exit(1)

    validate_base_input_data(base_data)

    # TODO: Add logic to find the base_computer instead of assuming it's first
    base_computer = NMSObject(base_data.get("Objects")[0])

    with Image.open(sprite_data_file) as image:
        validate_pixel_input_data(image)
        image = image.convert("RGB").quantize(palette=load_nes_palette())
        objects = sprite_data_to_objects(image, base_computer, z_up=z_up)

    # Update the JSON with new objects
    dict_objects = [nms_object.as_dict() for nms_object in objects]
    base_data.get("Objects").extend(dict_objects)

    logger.debug(f"Writing output JSON file to {output_file}")
    logger.debug("-=-=" * 10)

    with open(output_file, "w") as outfile:
        json.dump(base_data, outfile, indent=4)

    print("Success!")
