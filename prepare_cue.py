# process album to cue

# REM GENRE Pop
# REM DATE
# REM COMMENT "ExactAudioCopy v0.95b4"
# PERFORMER "Musica Nuda"
# TITLE "Loveless"
# FILE "01 - Come si canta una domanda.flac" WAVE
#   TRACK 01 AUDIO
#     TITLE "Come si canta una domanda"
#     INDEX 01 00:00:00

import sys
import re

genre = input("Please enter genre: ")
date = input("Please enter date: ")
performer = input("Please enter performer: ")
title = input("Please enter album: ")

cue_header = '''
REM GENRE %s
REM DATE %s
REM COMMENT "ExactAudioCopy v0.95b4"
PERFORMER "%s"
TITLE "%s"
''' % (genre, date, performer, title)

if __name__ == '__main__':
    source_file = sys.argv[1]
    if not source_file:
        print('Missing import file param')
        exit()

    try:
        with open(source_file, "r+") as f:
            data = f.read()

    except FileNotFoundError as err_str:
        print("\nFailed to open " + source_file)
        print(err_str)
        exit()

    file_pattern = r"\d+\s+(.*).flac"
    songs = [
        "FILE \"%s\" WAVE\n\tTRACK %02d AUDIO\n\t\tTITLE \"%s\"\n\t\tINDEX 01 00:00:00" %
        (file, c, re.findall(file_pattern, file)[0])
        for c, file in enumerate(data.split('\n'), 1)
    ]

    cue = cue_header + "\n".join(songs)

    file_mask = r"^(.*)\..+$"
    new_filename = re.findall(file_mask, source_file)[0] + ".cue"

    with open(new_filename, "w+") as f:
        f.write(cue)
        print('done')
