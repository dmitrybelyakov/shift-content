import click, os, sys, shutil
from boiler.cli.colors import *
import json
import os
from pprint import pprint as pp
from boiler.cli import get_app
from shiftcontent import content_service
import time

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
def ingest_data(path):
    """ Parse a directory to ingest sample content """

    # This will ingest a directory of sample blog posts in json format. You
    # can download sample data from: https://webhose.io/datasets/

    print(yellow('\nIngesting sample data'))
    print(yellow('-' * 80))

    if not os.path.isdir(path):
        print(red('This is not a directory: {}'.format(path)))
        return

    i = 0
    for file in os.listdir(path):
        i += 1

        time.sleep(0.05)

        filepath = os.path.join(path, file)
        with open(filepath) as fp:
            data = json.load(fp)

        preapared = dict(
            author_name=data['author'],
            published=data['published'],
            url=data['url'],
            title=data['thread']['title_full'],
            body=data['text'],
        )

        with get_app().app_context() as ctx:
            try:
                content_service.create_item(
                    content_type='blog_post',
                    author=1,
                    fields=preapared
                )
            except Exception as x:
                print(red('Error in file: {}: ({})'.format(filepath, str(x))))
                raise x
                pass

        msg = '{}. Ingested: {} ({})'
        print(green(msg.format(i, file, preapared['title'])))

    print()

