import path.structure
from models.record import MediaCenterRecord


class TVShow(MediaCenterRecord):
    def __init__(self, tvpath):
        super().__init__(tvpath, path.structure.MEDIA_TYPE_TV)


def get_tv_shows(tv_path):
    if tv_path.media_type != path.structure.MEDIA_TYPE_TV:
        raise ValueError('No TV shows in non-TV show path')
    for subpath in tv_path:
        tv_show = TVShow(subpath)
