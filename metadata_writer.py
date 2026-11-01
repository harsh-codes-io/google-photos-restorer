'''Use ExifTool to write metadata into images'''

import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def write_metadata(image_path: str | Path, metadata: dict) -> None:
    """Write supported metadata fields to an image."""

    image_path = Path(image_path)

    command = ["exiftool", "-overwrite_original"]

    # Restore capture date and time
    photo_taken_time = metadata.get("photo_taken_time")

    if isinstance(photo_taken_time, datetime):
        date_value = photo_taken_time.strftime("%Y:%m:%d %H:%M:%S")

        command.append(f"-DateTimeOriginal={date_value}")

        if photo_taken_time.utcoffset() is not None:
            offset = photo_taken_time.strftime("%z")
            offset = f"{offset[:3]}:{offset[3:]}"
            command.append(f"-OffsetTimeOriginal={offset}")

    # Restore GPS coordinates
    latitude = metadata.get("latitude")
    longitude = metadata.get("longitude")

    if latitude is not None and longitude is not None:
        command.append(f"-GPSLatitude={latitude}")
        command.append(f"-GPSLongitude={longitude}")

    # Restore description
    description = metadata.get("description")

    if description:
        command.append(f"-XMP-dc:Description={description}")

    if len(command) == 2:
        raise ValueError("No supported metadata fields were provided.")

    command.append(str(image_path))

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )

    print(result.stdout)


def create_image_copy(source_path: str | Path, output_directory: str | Path) -> Path:
    """Create a copy of an image in the output directory."""

    source_path = Path(source_path)
    output_directory = Path(output_directory)

    if not source_path.is_file():
        raise FileNotFoundError(f"Image not found: {source_path}")

    output_directory.mkdir(parents=True, exist_ok=True)

    destination_path = output_directory / source_path.name

    shutil.copy2(source_path, destination_path)

    return destination_path

def restore_image(source_path: str | Path,output_directory: str | Path, metadata: dict) -> Path:
    """Create a copy of an image and restore its metadata."""

    #Called create_image_copy() to create the copy of image 
    copied_image_path = create_image_copy(source_path,output_directory)

    #Called write_metadata() to write metadata to copied image file
    write_metadata(copied_image_path,metadata)

    return copied_image_path