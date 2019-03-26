import os

import path.structure
from path import helpers
from models.base import MediaCenterRecord


class Movie(MediaCenterRecord):
    movie_file = None
    other_dirs = []
    other_files = []

    def __init__(self, tvpath):
        super().__init__(tvpath, path.structure.MEDIA_TYPE_MOVIES)
        self._populate()

    def _populate(self):
        for fi in self:
            fi_type = helpers.get_file_type(fi)
            if fi_type is not None and 'video' in fi_type.mime:
                if self.movie_file is None:
                    self.movie_file = fi
                else:
                    stat = os.stat(fi)
                    compare = os.stat(self.movie_file)
                    if stat.st_size > compare.st_size:
                        self.movie_file = fi
            elif os.path.isdir(fi):
                self.other_dirs.append(fi)
            elif os.path.isfile(fi):
                self.other_files.append(fi)


def get_movies(movies_path):
    movies = []
    if movies_path.media_type != path.structure.MEDIA_TYPE_MOVIES:
        raise ValueError('No movies in non-movies path')
    for subpath in movies_path:
        movies.append(Movie(subpath))
    return movies
