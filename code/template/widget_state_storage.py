import os
import json
from datetime import datetime


STORAGE_FILE_PATH = ".answers.json"


def store_state(widget_type, identifier, state):
    if not os.path.isfile(STORAGE_FILE_PATH):
        data = {}
    else:
        with open(STORAGE_FILE_PATH, "r") as f:
            data = json.load(f)

    state["Zeitstempel"] = datetime.now().replace(microsecond=0).isoformat()
    
    key = _to_key(widget_type, identifier)
    data[key] = state

    with open(STORAGE_FILE_PATH, "w") as f:
        json.dump(data, f)


def load_state(widget_type, identifier, default_value=None):
    if os.path.isfile(STORAGE_FILE_PATH):
        with open(STORAGE_FILE_PATH, "r") as f:
            data = json.load(f)

            key = _to_key(widget_type, identifier)

            return data[key] if key in data else default_value

    return default_value


def _to_key(widget_type, identifier):
    return f"{widget_type}.{identifier}"