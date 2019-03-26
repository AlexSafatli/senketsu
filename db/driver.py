from db import drivers

DRIVER_NAME_AIRTABLE = 'Airtable'


def get_driver_by_name(driver_name):
    if driver_name == DRIVER_NAME_AIRTABLE:
        return drivers.airtable
    return None
