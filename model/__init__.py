# TODO: Consider having a SaveDataObject instead of just assuming dict type everywhere
import copy
import dataclasses
from typing import List


@dataclasses.dataclass
class NMSObject(object):
    """Represents the NMS object data found in the JSON output from
    NMSSaveEditor."""

    object_id: str = dataclasses.field(default_factory=str)
    position: list = dataclasses.field(default_factory=list)
    up: list = dataclasses.field(default_factory=list)
    at: list = dataclasses.field(default_factory=list)
    timestamp = 0
    userdata = 0
    message: str = dataclasses.field(default_factory=str)

    def __init__(self, obj_from_json_data: dict):
        self.up = obj_from_json_data.get("Up", [])
        self.timestamp = obj_from_json_data.get("Timestamp", "")
        self.at = obj_from_json_data.get("At", [])
        self.userdata = obj_from_json_data.get("UserData", 0)
        self.message = obj_from_json_data.get("Message", "")
        self.position = obj_from_json_data.get("Position", [])

    def get_z(self):
        """Get the z coordinate of the NMS object."""
        return self.position[2]

    def as_dict(self) -> dict:
        return {
            "ObjectID": self.object_id,
            "Position": self.position,
            "Up": self.up,
            "At": self.at,
            "Timestamp": self.timestamp,
            "UserData": self.userdata,
            "Message": self.message,
        }


def create_from_reference_object(
    reference_object: NMSObject, offsets: List[float], object_id, object_userdata
):
    """Creates a new NMSObject at the same position as the reference object, but shifted
    by the specified offsets and with the matching obj_type attributes."""
    this_obj = copy.copy(reference_object)
    this_obj.at = reference_object.at
    this_obj.up = reference_object.up
    # Sets the object type
    this_obj.object_id = object_id
    this_obj.timestamp = reference_object.timestamp
    # Set the userdata (color manipulation, etc.)
    this_obj.userdata = object_userdata
    this_obj.message = reference_object.message
    this_obj.position = [
        reference_object.position[0] + offsets[0],
        reference_object.position[1] + offsets[1],
        reference_object.position[2] + offsets[2],
    ]
    return this_obj
