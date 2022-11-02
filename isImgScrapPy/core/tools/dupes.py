"""
Module containing tools for managing/detecting/avoiding duplicate downloads.
"""
import glob


def gather_image_filepaths(start):
    image_paths = []
    for filename in glob.iglob(f'{start}**/*.jpg', recursive=True):
        print(filename)
        image_paths.append(filename)
    return image_paths


class DLHistory:
    def __init__(self):
        pass


