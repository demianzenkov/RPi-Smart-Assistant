# globals/__init__.py
_latest_video_filename = None
_latest_photo_filename = None

_latitude = None
_longitude = None


def set_latitude(latitude):
    global _latitude
    _latitude = latitude


def get_latitude():
    return _latitude


def set_longitude(longitude):
    global _longitude
    _longitude = longitude


def get_longitude():
    return _longitude


def set_latest_video_filename(filename):
    global _latest_video_filename
    _latest_video_filename = filename


def get_latest_video_filename():
    return _latest_video_filename


def set_latest_photo_filename(filename):
    global _latest_photo_filename
    _latest_photo_filename = filename


def get_latest_photo_filename():
    return _latest_photo_filename
