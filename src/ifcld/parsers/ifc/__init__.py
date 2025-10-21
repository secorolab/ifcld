import os
import json

_current_path = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(_current_path, "ifc4.offsets.json")) as f:
    OFFSETS = json.load(f)
with open(os.path.join(_current_path, "ifc4.ordered.json")) as f:
    ORDERED = json.load(f)
