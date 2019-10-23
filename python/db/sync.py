from path import structure


def sync_media_library_with_db(media_library, driver, config):
    written, deleted = [], []
    for media_type in structure.get_media_library_types():
        table_name = structure.get_media_library_type_label(media_type)
        if table_name is not None:
            conn = driver.new_connection(config, table_name)
            w, d = conn.mirror([media.to_dict() for media in
                                media_library.get_media_for_media_type(
                                    media_type)])
            written.extend(w)
            deleted.extend(d)
    if len(media_library.unformatted) > 0:
        conn = driver.new_connection(config, 'Unformatted')
        w, d = conn.mirror([media.to_dict() for media in
                            media_library.unformatted])
        written.extend(w)
        deleted.extend(d)
    return len(written), len(deleted)
