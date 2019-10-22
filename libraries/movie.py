import os

import path.structure
from libraries.base import MediaLocation
from path import helpers


class Movie(MediaLocation):
    __movie_file = None
    other_dirs = []
    other_files = []

    def __init__(self, tvpath):
        super().__init__(tvpath, path.structure.MEDIA_TYPE_MOVIES)

    def __populate(self):
        for fi in self:
            fi_type = helpers.get_file_type(fi)
            if fi_type is not None and 'video' in fi_type.mime:
                if self.__movie_file is None:
                    self.__movie_file = fi
                else:
                    stat = os.stat(fi)
                    compare = os.stat(self.__movie_file)
                    if stat.st_size > compare.st_size:
                        self.__movie_file = fi
            elif os.path.isdir(fi):
                self.other_dirs.append(fi)
            elif os.path.isfile(fi):
                self.other_files.append(fi)

    @property
    def movie_file(self):
        if self.__movie_file is None:
            self.__populate()
        return self.__movie_file


def get_movies(movies_path):
    movies = []
    if movies_path.media_type != path.structure.MEDIA_TYPE_MOVIES:
        raise ValueError('No movies in non-movies path')
    for subpath in movies_path:
        movies.append(Movie(subpath))
    return movies
