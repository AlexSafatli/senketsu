from path import structure


def write_media_library_to_db(media_library, driver, config):
    written = 0
    for media_type in structure.get_media_library_types():
        table_name = structure.get_media_library_type_label(media_type)
        if table_name is not None:
            conn = driver.new_connection(config, table_name)
            for media in media_library.get_media_for_media_type(media_type):
                d = media.to_dict()
                if driver.insert_unique_record(conn, 'Name', d['Name'], d):
                    written += 1
    if len(media_library.unformatted) > 0:
        conn = driver.new_connection(config, 'Unformatted')
        for media in media_library.unformatted:
            d = media.to_dict()
            if driver.insert_unique_record(conn, 'Name', d['Name'], d):
                written += 1
    return written


def delete_unknown_records_from_db(media_library, driver, config):
    deleted = 0
    for media_type in structure.get_media_library_types():
        table_name = structure.get_media_library_type_label(media_type)
        if table_name is not None:
            conn = driver.new_connection(config, table_name)
            records = driver.get_records(conn)
            media = media_library.get_media_for_media_type(media_type)
            names = list(map(lambda x: x.to_dict()['Name'], media))
            for record in records:
                if 'Name' in record and record['Name'] not in names:
                    driver.remove_record('Name', record['Name'])
                    deleted += 1
    conn = driver.new_connection(config, 'Unformatted')
    records = driver.get_records(conn)
    unformatted_names = list(map(lambda x: x.to_dict()['Name'],
                                 media_library.unformatted))
    for record in records:
        if 'Name' in record and record['Name'] not in unformatted_names:
            driver.remove_record('Name', record['Name'])
            deleted += 1
    return deleted


def sync_media_library_with_db(media_library, driver, config):
    deleted = delete_unknown_records_from_db(media_library, driver, config)
    written = write_media_library_to_db(media_library, driver, config)
    return written, deleted
