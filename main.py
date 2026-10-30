from json import JSONDecodeError
from pathlib import Path

import metadata_reader as mr
import scanner

# Give path of current python file(main.py in this case) and creating Path object
script_path = Path(__file__)
# using .resolve() to obtain an absolute path of the directory in which script is located
project_dir = script_path.resolve().parent
json_file_path = project_dir / "sample.json"
#print("Parsing JSON file:")

directory = project_dir / "sample_data"

# Step 1: Discover media files and JSON sidecars
files = scanner.scan_directory(directory)

# Step 2: Match media files with their sidecars
matched_files = scanner.match_sidecars(files)

try:
    parsed_json = mr.read_json(json_file_path)
    extracted_data = mr.extract_metadata(parsed_json)
except FileNotFoundError:
    print("JSON file Could not be found.")
except JSONDecodeError:
    print("JSON file found but contains invalid JSON data")
except KeyError as error:
    print(f"Invalid metadata: {error}")
else:
    print(f"Photo Title: {extracted_data['title']}")
    print(f"Photo Description: {extracted_data['description']}")
    print(f"Photo Taken Time: {extracted_data['photo_taken_time']}")
