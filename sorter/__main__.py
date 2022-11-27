from sorter.utils.gdrive.gdrive_helper import GoogleDrive
from sorter.utils.Regex_utils.regex_helper import AnimeRegex
import signal

def keyboard_exit(signal, frame):
    print("Exiting....")
    exit(0)

signal.signal(signal.SIGINT, keyboard_exit)

anime_regex = AnimeRegex(GoogleDrive)
anime_regex.match_by_regex()

