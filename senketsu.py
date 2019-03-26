import click


@click.group()
def main():
    pass


@main.group()
def crawl():
    pass


@main.group()
def rename():
    pass


@rename.command()
@click.argument('path')
def tv(path):
    pass


if __name__ == '__main__':
    main()
