'''Find media files and JSON sidecars'''

from pathlib import Path

directory = Path("sample_data")
#discovers supported media files and JSON sidecars.
def scan_directory(directory: Path) -> list[Path]: 
    files = []
    extensions = [".heic",".jpeg",".jpg",".png"]
    media_files = [item for item in directory.iterdir() if item.is_file() and item.suffix.lower() in extensions]
    json_files = [item for item in directory.iterdir() if item.is_file() and item.suffix.lower() == ".json"]

    files.extend(media_files)
    files.extend(json_files)

    return files

#matches media files with their corresponding sidecars.
def match_sidecars(files: list[Path]) -> dict[Path,Path]:
    json_files = {}
    media_and_json = {}
    #creating dictionay having json file name as key and its path as object :[str:Path]
    for j_file in files:
        if j_file.suffix.lower() == ".json":
            json_files[j_file.name] = j_file

    # using dictionary lookup to match the media file with corresponding json file and created a dictionary: dict{media file: matching json}
    for m_file in files:
        if m_file.suffix.lower() != ".json":
            expected_file = m_file.name + ".json"
            matching_json = json_files.get(expected_file)
            if matching_json is None:
                expected_file= m_file.stem+".metadata.json"
                matching_json = json_files.get(expected_file)
        else:
            continue

        if(matching_json):
            media_and_json[m_file] = matching_json

    return media_and_json


    

files_list = scan_directory(directory)
print(match_sidecars(files_list))

