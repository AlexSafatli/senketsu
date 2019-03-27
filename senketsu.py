import click

import os

import config
import models.base
import db.driver
import db.sync


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
    click.echo('Reading file system (%s) to populate media library...' %
               root_path)
    library = models.base.MediaLibrary(root_path)
    click.echo('Found %d formatted media records...' % len(library))
    drive = db.driver.get_driver_by_name(driver)
    w, d = db.sync.sync_media_library_with_db(library, drive, config.CONFIG)
    click.echo('Deleted %d records from %s' % (d, driver))
    click.echo('Wrote %d records to %s' % (w, driver))


if __name__ == '__main__':
    main()
