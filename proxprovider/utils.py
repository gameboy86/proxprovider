import re


def convert_name(name):
    return re.sub('(?!^)([A-Z]+)', r'_\1', name).lower()
