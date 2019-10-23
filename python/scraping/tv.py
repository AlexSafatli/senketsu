import tvdb_api


def get_tvdb_api_connection():
    return tvdb_api.Tvdb()


def get_tv_show(show_name, tvdb) -> tvdb_api.Show or None:
    try:
        show = tvdb[show_name]
    except tvdb_api.tvdb_error:
        return None
    except tvdb_api.tvdb_shownotfound:
        return None
    return show


def get_tv_show_rating(tv_show: tvdb_api.Show) -> float:
    return tv_show['siteRating']
