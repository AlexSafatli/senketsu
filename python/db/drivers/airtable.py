from airtable import Airtable


def new_connection(config, table_name):
    base_name = config['airtable_base_name']
    return Airtable(config['airtable_base_' + base_name.lower() + '_key'],
                    table_name, api_key=config['airtable_api_key'])


def get_records(table):
    return list(map(lambda x: x['fields'], table.get_all()))


def insert_unique_record(table, key_field, key_value, data):
    search = table.search(key_field, key_value)
    if not search:
        table.insert(data)
        return True
    return table.replace(search[0]['id'], data)


def remove_record(table, key_field, key_value):
    if table.search(key_field, key_value):
        table.delete_by_field(key_field, key_value)
        return True
    return False


def mirror_records(table, records):
    return table.mirror(records)


def get_database_path(base_name, table_name):
    return base_name + '/' + table_name
