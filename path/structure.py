from path import helpers

import os

MEDIA_TYPE_UNKNOWN = 0
MEDIA_TYPE_TV = 1
MEDIA_TYPE_MOVIES = 2
MEDIA_TYPE_ANIME = 3
MEDIA_TYPE_CHILD = 4

NOT_FORMATTED = '(Not Formatted)'
LABEL_TV = 'TV Shows'
LABEL_MOVIES = 'Movies'
LABEL_ANIME = 'Anime'


class MediaCenterPath(object):
    path = ''
    media_type = MEDIA_TYPE_UNKNOWN
    formatted = True

    def __init__(self, path, mtype, formatted):
        self.path = path
        self.media_type = mtype
        self.formatted = formatted

    @property
    def name(self):
        return helpers.get_file_name_parts(self.path)[0]

    @property
    def extension(self):
        return helpers.get_file_name_parts(self.path)[1]

    def __len__(self):
        return len(helpers.get_files_in_path(self.path))

    def __iter__(self):
        for fi in helpers.get_files_in_path(self.path):
            yield fi

    def __getitem__(self, item):
        for fi in self:
            if item in helpers.get_file_name_parts(fi)[0]:
                return fi


def get_media_library_paths(root_path):
    library = []
    for fi in helpers.get_files_in_path(root_path):
        if os.path.isdir(fi):
            name = helpers.get_file_name_parts(fi)[0]
            mtype = MEDIA_TYPE_UNKNOWN
            if LABEL_TV in name:
                mtype = MEDIA_TYPE_TV
            elif LABEL_MOVIES in name:
                mtype = MEDIA_TYPE_MOVIES
            elif LABEL_ANIME in name:
                mtype = MEDIA_TYPE_ANIME
            library_path = MediaCenterPath(fi, mtype, NOT_FORMATTED in name)
            library.append(library_path)
    return library
