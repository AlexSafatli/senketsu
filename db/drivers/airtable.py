from airtable import Airtable


def new_connection(config, table_name):
    base_name = config['airtable_base_name']
    return Airtable(config['airtable_base_' + base_name.lower() + '_key'],
                    table_name, api_key=config['airtable_api_key'])


def get_records(table):
    return table.get_all()


def insert_unique_record(table, key_field, key_value, data):
    if not table.search(key_field, key_value):
        table.insert(data)
        return True
    return False


def remove_record(table, key_field, key_value):
    if table.search(key_field, key_value):
        table.delete_by_field(key_field, key_value)
        return True
    return False


def get_database_path(base_name, table_name):
    return base_name + '/' + table_name
