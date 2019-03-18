import click


@click.group()
def main():
    pass


@main.group()
def rename():
    pass


@rename.command()
@click.argument('path')
def tv(path):
    if database.insert_unique_record(table, 'Name', thing, data):
        click.echo("Inserted %s into %s" % (thing, path))
    else:
        click.echo("Already found name %s in %s" % (thing, path))


if __name__ == '__main__':
    main()
