import os
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
import datetime
import shutil


file_extensions = ('.jpg', '.jpeg', '.heic', '.cr2', '.mov', '.mp4', '.png', '.avi')
image_extensions = ('.jpg', '.jpeg', '.heic', '.cr2')

def get_date(image_path):
    if image_path.lower().endswith(image_extensions):
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag == "DateTimeOriginal":
                            return datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except Exception as e:
            print(f"Error processing EXIF data for {image_path}: {str(e)}")

    # Fallback to file creation date
    try:
        creation_time = os.path.getctime(image_path)
        modification_time = os.path.getmtime(image_path)
        oldest_time = min(creation_time, modification_time)
        return datetime.datetime.fromtimestamp(oldest_time)
    except Exception as e:
        print(f"Error getting file dates for {image_path}: {str(e)}")

    return None

def process_image_files(file_list, destination_directory):
    copied_log = open("copied.log", "w")
    not_copied_log = open("not_copied.log", "w")
    skipped_log = open("skipped.log", "w")
    overwritten_log = open("overwritten.log", "w")

    for file_path in file_list:
        file_path = file_path.strip()  # Remove any leading/trailing whitespace
        if os.path.isfile(file_path) and file_path.lower().endswith(file_extensions):
            try:
                date = get_date(file_path)
            except Exception as e:
                print(f"Error reading file {file_path}: {str(e)}")
                raise

            if date:
                # Create destination path
                dest_path = os.path.join(
                    destination_directory,
                    date.strftime("%Y"),
                    date.strftime("%Y-%m-%d"),
                    date.strftime("%Y%m%d_%H%M%S") + os.path.splitext(os.path.basename(file_path))[1]
                )

                # Check if destination file already exists
                if os.path.exists(dest_path):
                    source_size = os.path.getsize(file_path)
                    dest_size = os.path.getsize(dest_path)
                    if source_size > dest_size:
                        try:
                            shutil.copy2(file_path, dest_path)
                        except Exception as e:
                            print(f"Error copying file {file_path} to {dest_path}: {str(e)}")
                            raise
                        overwritten_log.write(f"{file_path} -> {dest_path} (overwritten)\n")
                        print(f"Overwritten (larger file): {file_path} -> {dest_path}")
                    else:
                        skipped_log.write(f"{file_path} -> {dest_path} (already exists, not larger)\n")
                        print(f"Skipped (already exists, not larger): {file_path}")
                else:
                    # Ensure destination directory exists
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                    # Copy file
                    try:
                        shutil.copy2(file_path, dest_path)
                    except Exception as e:
                        print(f"Error copying file {file_path} to {dest_path}: {str(e)}")
                        raise
                    copied_log.write(f"{file_path} -> {dest_path}\n")
                    print(f"Copied: {file_path} -> {dest_path}")
            else:
                not_copied_log.write(f"{file_path}\n")
                print(f"Not copied (no date): {file_path}")
        else:
            not_copied_log.write(f"{file_path} (not a valid jpg file)\n")
            print(f"Not copied (not a valid jpg file): {file_path}")    

    copied_log.close()
    not_copied_log.close()
    skipped_log.close()
    overwritten_log.close()

def read_source_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and organize image files.")
    parser.add_argument("--source-file", help="Path to a text file containing a list of image files to process")
    parser.add_argument("--source-directory", help="Directory containing images to process")
    parser.add_argument("--destination-directory", required=True, help="Directory to store organized images")
    args = parser.parse_args()

    if not os.path.isdir(args.destination_directory):
        print(f"Error: {args.destination_directory} is not a valid directory")
        exit(1)

    if args.source_file:
        if not os.path.isfile(args.source_file):
            print(f"Error: {args.source_file} is not a valid file")
            exit(1)
        file_list = read_source_file(args.source_file)
        process_image_files(file_list, args.destination_directory)
    elif args.source_directory:
        if not os.path.isdir(args.source_directory):
            print(f"Error: {args.source_directory} is not a valid directory")
            exit(1)
        file_list = []
        for root, dirs, files in os.walk(args.source_directory):
            for file in files:
                if file.lower().endswith(file_extensions):
                    file_list.append(os.path.join(root, file))
        process_image_files(file_list, args.destination_directory)
    else:
        print("Error: Either --source-file or --source-directory must be provided")
        exit(1)