'''Reads the JSON file and extract the required data'''

import json
from datetime import datetime, timezone
from pathlib import Path


def read_json(file_path : str | Path) -> dict:
    with open(file_path,"r") as file:
        file_data = json.load(file)

    return file_data


def extract_metadata(data: dict) -> dict:
    extracted_fields = {}

    if "title" not in data:
        raise KeyError("Required field 'title' is missing from JSON data")

    extracted_fields['title'] = data.get("title")
    extracted_fields['description'] = data.get("description")
    extracted_fields['photo_taken_time'] = convert_timestamp(data.get("photoTakenTime", {}).get("timestamp"))

    return extracted_fields

def convert_timestamp(timestamp: str | None) -> datetime | None:
    try:
        timestamp = int(timestamp)
        dateobj = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dateobj

    except (TypeError, ValueError, OverflowError, OSError):
        #TypeError -> if None
        #ValueErrors -> if not a timestamp
        #overflowError, OSError - > if timestamp int is "000000000678990"
        return None
    
    
    