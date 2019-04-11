import tvdb_api


def get_tvdb_api_connection():
    return tvdb_api.Tvdb()


def get_tv_show(show_name, tvdb):
    try:
        show = tvdb[show_name]
    except tvdb_api.tvdb_error:
        return None
    except tvdb_api.tvdb_shownotfound:
        return None
    return show

