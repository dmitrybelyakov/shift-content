import click, os, sys, shutil
from boiler.cli.colors import *
import json
import os
from pprint import pprint as pp

# -----------------------------------------------------------------------------
# Group setup
# -----------------------------------------------------------------------------


@click.group(help=yellow('ShiftContent CLI'))
def cli():
    pass


# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------

@cli.command(name='ingest-data')
@click.argument('path')
def test(path):
    """ Parse a directory to ingest sample content (see notes) """

    # This will ingest a directory of sample blog posts in json format. You
    # can download sample data from: https://webhose.io/datasets/

    print(yellow('\nIngesting sample data'))
    print(yellow('-' * 80))

    if not os.path.isdir(path):
        print(red('This is not a directory: {}'.format(path)))
        return

    i = 0
    for file in os.listdir(path):
        with open(os.path.join(path, file)) as fp:
            data = json.load(fp)

        i += 1
        print(green('{}. Ingested: {}'.format(i, file)))

        preapared = dict(
            author_name=data['author'],
            published=data['published'],
            url=data['url'],
            title=data['thread']['title_full'],
            body=data['text'],
        )

        # pp(preapared)
        # break



    print()