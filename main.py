from json import JSONDecodeError
from pathlib import Path

import metadata_reader as mr
import scanner


def main() -> None:
    # Give path of current python file(main.py in this case) and creating Path object
    script_path = Path(__file__)
    # using .resolve() to obtain an absolute path of the directory in which script is located
    project_dir = script_path.resolve().parent
    #json_file_path = project_dir / "sample.json"
    #print("Parsing JSON file:")

    directory = project_dir / "sample_data"

    # Step 1: Scan the directory - Discover media files and JSON sidecars
    files = scanner.scan_directory(directory)

    # Step 2: Match media files with their sidecars
    matched_files = scanner.match_sidecars(files)

    for media_file_path , json_file_path in matched_files.items():
        try:
            parsed_json = mr.read_json(json_file_path)
            extracted_data = mr.extract_metadata(parsed_json)
            print(f"\nProcessing photo: {media_file_path.name}")
        except FileNotFoundError:
            print("JSON file Could not be found.")
        except JSONDecodeError:
            print(f"Invalid JSON data in: {json_file_path.name}")
        except KeyError as error:
            print(f"Invalid metadata: {error}")
        else:
            print(f"Photo Title: {extracted_data['title']}")
            print(f"Photo Description: {extracted_data['description']}")
            print(f"Photo Taken Time: {extracted_data['photo_taken_time']}")

if __name__ == "__main__":
    main()

