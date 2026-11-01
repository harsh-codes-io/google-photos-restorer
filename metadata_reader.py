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

    timestamp=safe_extract_timestamp(data)
    extracted_fields["photo_taken_time"] = convert_timestamp(timestamp)

    extracted_fields['latitude'] = safe_extract_coordinates(data,"latitude")
    extracted_fields['longitude'] = safe_extract_coordinates(data,"longitude")

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

def safe_extract_timestamp(data: dict) -> str | None:
    photo_taken_time = data.get("photoTakenTime")
    
    if isinstance(photo_taken_time, dict):
        return photo_taken_time.get("timestamp")
    else:
        return None 

def safe_extract_coordinates(data: dict,coordinate: str) -> float | int | None:
    geo_data = data.get("geoData")

    if isinstance(geo_data, dict):
        return geo_data.get(coordinate)

    else:
        return None 
    

    
    

    
    
    