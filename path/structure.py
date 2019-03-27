from path import helpers

import os

MEDIA_TYPE_UNKNOWN = 0
MEDIA_TYPE_TV = 1
MEDIA_TYPE_MOVIES = 2
MEDIA_TYPE_ANIME = 3
MEDIA_TYPE_DRAMA = 4
MEDIA_TYPE_CHILD = 5

NOT_FORMATTED = '(Not Formatted)'
LABEL_TV = 'TV Series'
LABEL_MOVIES = 'Movies'
LABEL_ANIME = 'Anime'
LABEL_DRAMA = 'Dramas'


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
            elif LABEL_DRAMA in name:
                mtype = MEDIA_TYPE_DRAMA
            library.append(MediaCenterPath(fi, mtype,
                                           not (NOT_FORMATTED in name)))
    return library


def get_media_library_types():
    return [MEDIA_TYPE_TV, MEDIA_TYPE_MOVIES, MEDIA_TYPE_ANIME,
            MEDIA_TYPE_DRAMA]


def get_media_library_type_label(media_type):
    if media_type == MEDIA_TYPE_TV:
        return LABEL_TV
    elif media_type == MEDIA_TYPE_MOVIES:
        return LABEL_MOVIES
    elif media_type == MEDIA_TYPE_ANIME:
        return LABEL_ANIME
    elif media_type == MEDIA_TYPE_DRAMA:
        return LABEL_DRAMA
    return None
