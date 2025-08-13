from constants import BASE_FLAG_ID, MAX_BASE_OBJS


class IncompatibleImageError:
    pass


def validate_pixel_input_data(pixel_input_data):
    """Confirm that the pixel data adheres to the limitations we impose"""

    # Limit of 3000 pixels
    width, height = pixel_input_data.size
    if width * height > MAX_BASE_OBJS:
        raise ImageTooBigError

    # Confirm quantization compat the laziest way ever
    try:
        pixel_input_data.quantize(colors=256)
    except ValueError:
        raise IncompatibleImageError


def validate_base_input_data(base_input_data: dict):
    """Performs some basic checks to make sure the input JSON is valid"""
    if base_input_data.get("Objects", None) is None:
        print("Objects array in base data was not found")
        raise InvalidBaseDataError

    # Base computer should be the first object in the array or this won't work as expected
    if base_input_data.get("Objects")[0].get("ObjectID") != BASE_FLAG_ID:
        print("First object was not the base computer, this base is unsupported atm")
        raise InvalidBaseDataError

    # TODO: Once we've made the logic more flexible, just check that a base computer is
    # present


class InvalidBaseDataError(Exception):
    pass


class CorruptedBaseDataError(Exception):
    pass


class ImageTooBigError(Exception):
    pass
