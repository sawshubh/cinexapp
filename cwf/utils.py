import json
import datetime
import uuid
import sys
import re


def get_environment(request_obj):
    environment = "development"
    url = request_obj.META.get("HTTP_HOST")

    if url.find("cinex2.com") != -1:  # not purchased yet
        environment = "production"

    return environment


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, "isoformat") else obj


def json_dumps(obj):
    return json.dumps(obj, default=date_handler)


def get_utc_timestamp():
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.%f")


def get_uuid():
    return str(uuid.uuid4())


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, "__dict__"):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def is_ajax_request(request):
    """Is this a ajax request?"""
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def is_valid_email(email):
    """Check if the email is a valid format."""
    # Regular expression for validating an Email
    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    # If the string matches the regex, it is a valid email
    if re.match(regex, email):
        return True
    else:
        return False
