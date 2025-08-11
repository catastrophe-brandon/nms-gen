# TODO: Consider having a SaveDataObject instead of just assuming dict type everywhere
import dataclasses


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
