from bson import ObjectId
def convert_object_ids(data):
    if isinstance(data, dict):
        return {
            key: convert_object_ids(value)
            for key, value in data.items()
        }

    if isinstance(data, list):
        return [
            convert_object_ids(item)
            for item in data
        ]

    if isinstance(data, ObjectId):
        return str(data)

    return data

def categorical_match(value1, value2):
    """
    Compare two categorical values.

    Returns:
    1.0  -> exact match
    0.5  -> one side has no preference
    0.0  -> mismatch
    """

    if value1 == value2:
        return 1.0

    if value1 == "no_preference" or value2 == "no_preference":
        return 0.5

    return 0.0


def numerical_similarity(value1, value2, max_difference=4):
    """
    Compare two numerical values.

    Example:
    5 and 5 -> 1.0
    5 and 4 -> 0.75
    5 and 1 -> 0.0
    """

    if value1 is None or value2 is None:
        return 0.0

    difference = abs(value1 - value2)

    score = 1 - (difference / max_difference)

    return max(0.0, score)


def time_difference(time1, time2):
    """
    Calculate circular difference between two times.

    Example:
    23:00 and 00:00 -> 60 minutes
    23:00 and 07:00 -> 480 minutes
    """

    if not time1 or not time2:
        return None

    h1, m1 = map(int, time1.split(":"))
    h2, m2 = map(int, time2.split(":"))

    minutes1 = h1 * 60 + m1
    minutes2 = h2 * 60 + m2

    difference = abs(minutes1 - minutes2)

    # Handle midnight crossing
    difference = min(difference, 1440 - difference)

    return difference


def sleep_similarity(time1, time2):
    """
    Convert sleep-time difference into a score between 0 and 1.

    Same time       -> 1.0
    1 hour difference -> 0.875
    4 hours difference -> 0.5
    8+ hours difference -> 0.0
    """

    difference = time_difference(time1, time2)

    if difference is None:
        return 0.0

    max_difference = 8 * 60

    score = 1 - (difference / max_difference)

    return max(0.0, score)

def preference_match(value1, value2):
    """
    Compare lifestyle preferences such as guests/pets.

    Exact match -> 1.0
    No preference -> 0.5
    Otherwise -> 0.0
    """

    if value1 == value2:
        return 1.0

    if value1 == "no_preference" or value2 == "no_preference":
        return 0.5

    return 0.0
def age_match(age, min_age, max_age):
    """
    Check whether the seeker's age
    falls within the owner's preferred age range.
    """

    if age is None:
        return 0.0

    if min_age is not None and age < min_age:
        return 0.0

    if max_age is not None and age > max_age:
        return 0.0

    return 1.0


def gender_match(seeker_gender, preferred_gender):
    """
    Check whether seeker's gender
    matches owner's preference.
    """

    if preferred_gender == "no_preference":
        return 0.5

    if seeker_gender == preferred_gender:
        return 1.0

    return 0.0

def location_similarity(area1, area2):
    """
    Compare two areas.

    Same area       -> 1.0
    Different area  -> 0.0
    Missing area    -> 0.0
    """

    if not area1 or not area2:
        return 0.0

    if area1.lower() == area2.lower():
        return 1.0

    return 0.0