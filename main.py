import os
import json
from PIL import Image

def load_base_json(file_path) -> dict:
    """Loads the base data JSON"""
    with open(file_path, 'r') as json_data:
        our_data_file = json.load(json_data)
        return our_data_file

class InvalidBaseDataError(Exception):
    pass

class CorruptedBaseDataError(Exception):
    pass

class NMSObject(object):

    object_id = ""
    position = []
    up = []
    at = []
    timestamp = 0
    userdata = 0
    message = ""

    def __init__(obj_from_json_data):
        # base is assumed to be the first object in the array
        root = obj_from_json_data("Objects")[0]
        self.pos = root.get("Position")
        self.up = root.get("Up")
        self.timestamp = root.get("Timestamp")
        self.at= root.get("At")
        self.userdata = root.get("UserData")
        self.message = root.get("Message")


BASE_FLAG_ID = "^BASE_FLAG"

class BaseComputer(NMSObject):

    def __init__(base_computer_data:dict):
        if base_computer_data.get("Objects")[0].get("ObjectId") != BASE_FLAG_ID:
            raise CorruptedBaseDataError

        super(base_computer_data.get("Objects"[0]))

    def get_z():
        return self.pos[2]

def validate_base_input_data(base_input_data: dict):
    """Performs some basic checks to make sure the input JSON is valid"""
    if base_input_data.get("Objects", None) is None:
        raise InvalidBaseDataError

    # Base computer should be the first object in the array
    if base_input_data.get("Objects")[0].get("ObjectId") != BASE_FLAG_ID:
        raise InvalidBaseDataError


def sprite_data_to_objects(sprite_data_file, base_computer):
    with Image.open(sprite_data_file) as image:
        image.verify()
        pixels = list(im.getdata())
        width, height = im.size


    pass


if __name__ == '__main__':

    # path to base data json file
    base_data_file = ""

    # path to sprite data file
    sprite_data_file = ""
   
    try:
        base_data = load_base_json(base_data_file)
    except:
        print(f"An error occurred when trying to load base json data from {base_data_file}")
        exit(1)

    # check that there is an array of objects in the right place
    validate_base_input_data(base_data)

    # Use base computer as our "origin"
    base_computer = BaseComputer(base_data)

    # Confirm the sprite data file exists and is readable
    try: 
        with open(sprite_data_file, 'r') as sprite_data_file:
            objects = sprite_data_to_objects(sprite_data_file, base_computer)
    except:
        print(f"An error occured trying to process the image input file {sprite_data_file}"
        exit(1)



    
