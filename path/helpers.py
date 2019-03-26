import filetype

from glob import glob
import os


def get_files_in_path(path, glob_pattern='*'):
    return glob(os.path.join(path, glob_pattern))


def get_file_name_parts(path):
    spl = os.path.splitext(os.path.basename(path))
    return spl[0], spl[1]


def get_file_type(path):
    return filetype.guess(path)
