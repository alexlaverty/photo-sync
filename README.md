# Photo Sync

This Python script organizes image and video files by date, copying them into a structured directory based on their creation date. It supports various file types and uses intelligent date detection methods.

## Features

- Organizes images and videos by date
- Supports multiple file formats: .jpg, .jpeg, .heic, .cr2, .mov, .mp4, .png, .avi
- Intelligent date detection using EXIF data and file metadata
- Handles duplicate files by comparing file sizes
- Generates detailed logs of processed files

## Requirements

- Python 3.x
- Pillow library (`pip install Pillow`)

## Usage

```
python photo-sync.py --source-file <path_to_source_file> --destination-directory <path_to_destination>
```
or
```
python photo-sync.py --source-directory <path_to_source_directory> --destination-directory <path_to_destination>
```

### Arguments

- `--source-file`: Path to a text file containing a list of image files to process
- `--source-directory`: Directory containing images to process
- `--destination-directory`: Directory to store organized images (required)

## Date Detection Logic

The script uses the following logic to determine the date of each file:

1. For image files (.jpg, .jpeg, .heic, .cr2):
   a. First, it attempts to read the "DateTimeOriginal" tag from the EXIF data.
   b. If EXIF data is not available or doesn't contain the date, it falls back to file metadata.

2. For all file types (including non-image files):
   a. If EXIF data is not available or the file is not an image, it uses the earlier of the file's creation time and modification time.

3. If no date can be determined, the file is logged as "not copied" and skipped.

## File Organization

Files are organized in the destination directory using the following structure:

```
destination_directory/
    YYYY/
        YYYY-MM-DD/
            YYYYMMDD_HHMMSS.ext
```

## Duplicate Handling

When a file with the same name already exists in the destination:

1. The script compares the file sizes of the source and destination files.
2. If the source file is larger, it overwrites the destination file and logs this action.
3. If the source file is not larger, it skips the file and logs it as skipped.

## Logs

The script generates four log files:

- `copied.log`: Successfully copied files
- `not_copied.log`: Files that couldn't be copied (e.g., no date found)
- `skipped.log`: Files skipped due to existing larger or equal-sized files in the destination
- `overwritten.log`: Files that were overwritten in the destination due to larger source files

## Notes

- Ensure you have sufficient permissions to read from the source and write to the destination.
- The script does not delete any files from the source location.
- It's recommended to run the script on a copy of your files first to ensure it behaves as expected.

## License

[Specify your license here]