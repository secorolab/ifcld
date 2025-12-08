import os
import json

_current_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(_current_path, "ifc-metamodel.json")) as f:
    METAMODEL = json.load(f)
with open(os.path.join(_current_path, "prov.json")) as f:
    PROV_METAMODEL = json.load(f)
