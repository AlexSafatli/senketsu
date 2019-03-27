import re

import path.helpers
import path.structure
import models


class MediaLibrary(object):
    __library_paths = list()
    root_path = ''
    tv_shows = list()
    movies = list()
    anime = list()
    dramas = list()
    unformatted = list()

    def __init__(self, root_path):
        self.root_path = root_path
        self.__library_paths = path.structure.get_media_library_paths(root_path)
        self._populate()

    def __len__(self):
        return len(self.tv_shows) + len(self.movies) + len(self.anime) + \
               len(self.dramas)

    def _populate(self):
        for p in self.__library_paths:
            if p.media_type == path.structure.MEDIA_TYPE_TV:
                if p.formatted:
                    self.tv_shows.extend(models.tv.get_tv_shows(p))
                else:
                    self.unformatted.extend(models.tv.get_tv_shows(p))
            elif p.media_type == path.structure.MEDIA_TYPE_MOVIES:
                if p.formatted:
                    self.movies.extend(models.movie.get_movies(p))
                else:
                    self.unformatted.extend(models.movie.get_movies(p))
            elif p.media_type == path.structure.MEDIA_TYPE_ANIME:
                if p.formatted:
                    self.anime.extend(models.anime.get_anime_shows(p))
                else:
                    self.unformatted.extend(models.anime.get_anime_shows(p))
            elif p.media_type == path.structure.MEDIA_TYPE_DRAMA:
                if p.formatted:
                    self.dramas.extend(models.dramas.get_dramas(p))
                else:
                    self.unformatted.extend(models.dramas.get_dramas(p))

    def get_media_for_media_type(self, media_type):
        if media_type == path.structure.MEDIA_TYPE_TV:
            return self.tv_shows
        elif media_type == path.structure.MEDIA_TYPE_MOVIES:
            return self.movies
        elif media_type == path.structure.MEDIA_TYPE_ANIME:
            return self.anime
        elif media_type == path.structure.MEDIA_TYPE_DRAMA:
            return self.dramas
        return list()


class MediaLocation(path.structure.MediaCenterPath):
    __size = None
    __clean_name = ''

    def __init__(self, mpath, mtype):
        super().__init__(mpath, mtype, True)
        self.__clean_name = re.sub(r'[^a-zA-Z0-9()\- ]', '', self.name)

    @property
    def clean_name(self):
        return self.__clean_name

    @property
    def file_size(self):
        if self.__size is None:
            self.__size = path.helpers.get_folder_size(self.path)
        return self.__size

    def to_dict(self):
        return {
            'Name': self.clean_name,
            'Type': path.structure.get_media_library_type_label(
                self.media_type),
            'Path': self.path,
            'Size': self.file_size * 1.0e-9
        }
