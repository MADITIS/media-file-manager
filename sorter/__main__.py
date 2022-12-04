from sorter.utils.gdrive.gdrive_helper import AnimeGoogleDrive
from sorter.utils.Regex_utils.regex_helper import AnimeRegex
import signal

def keyboard_exit(signal, frame):
    print("Exiting....")
    exit(0)

signal.signal(signal.SIGINT, keyboard_exit)

anime_regex = AnimeRegex(AnimeGoogleDrive)
anime_regex.match_by_regex()

# drive = AnimeGoogleDrive()
# print(drive.is_folder_exist('test', '1mB1PUbkxXfl1o4RJO5l9_VBGZ7WGiIj2'))
