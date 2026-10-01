from bson import ObjectId


def is_valid_object_id(value):
    """
    Check whether a value is a valid MongoDB ObjectId.
    """

    return ObjectId.is_valid(value)