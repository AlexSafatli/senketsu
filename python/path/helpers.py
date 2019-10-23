import filetype

from sre_constants import error
from glob import glob
import os


def get_files_in_path(path, glob_pattern='*'):
    try:
        return glob(os.path.join(path, glob_pattern))
    except error:
        return []


def get_file_name_parts(path):
    spl = os.path.splitext(os.path.basename(path))
    return spl[0], spl[1]


def get_file_type(path):
    if os.path.isfile(path):
        return filetype.guess(path)


def get_folder_size(folder_path):
    if not os.path.isdir(folder_path):
        raise OSError('%s not a directory' % folder_path)
    total_size = 0
    for dirpath, dirnames, fnames in os.walk(folder_path):
        for f in fnames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size
