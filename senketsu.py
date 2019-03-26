import click

import os

import config
import models.base
import db.driver
import db.writer


@click.group()
def main():
    pass


@main.group()
def database():
    pass


@database.command()
@click.argument('root_path')
@click.option('-d', '--driver', type=click.Choice(['Airtable']),
              default='Airtable')
def sync(root_path, driver):
    if not os.path.isdir(root_path):
        raise OSError('Path %s not found' % root_path)
    library = models.base.MediaLibrary(root_path)
    d = db.driver.get_driver_by_name(driver)
    wr, deleted = db.writer.sync_media_library_with_db(
        library, d, config.CONFIG)
    click.echo('Wrote %d records to %s' % (wr, driver))
    click.echo('Deleted %d records from %s' % (deleted, driver))


if __name__ == '__main__':
    main()
