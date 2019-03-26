from path import structure


def write_media_library_to_db(media_library, driver, config):
    written = 0
    for media_type in structure.get_media_library_types():
        table_name = structure.get_media_library_type_label(media_type)
        if table_name is not None:
            conn = driver.new_connection(config, table_name)
            for media in media_library.get_media_for_media_type(media_type):
                if (driver.insert_unique_record(conn, 'Name', media.name,
                                                media.to_dict())):
                    written += 1
    return written
