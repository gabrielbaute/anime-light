import os

def count_files_in_directory(directory: str):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            count += 1
    return count