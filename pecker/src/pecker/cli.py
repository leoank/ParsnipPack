import click
from pecker.scrape import scrape as _scrape


@click.command()
def scrape():
    _scrape()


@click.group()
def main():
    """Pecker CLI"""
    pass


main.add_command(scrape)
