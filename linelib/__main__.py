"""
Create your first linelib project through your terminal.
"""
from __future__ import annotations

import click # pip install click
import requests # pip install requests
import uuid
import os
import time
import sys

from flask import Flask

"""
Configure here!
"""
AVAILABLE_EXAMPLES = {
    'hello': [
        'https://gist.githubusercontent.com/AWeirdScratcher/8ddac68554328b8beaa139d8c4f01e79/raw/ca669b3b37ee4952ea370270de802ff08025957d/main.py'
    ]
}
FILE_NAMES = {
    'hello': ['main.py']
}



@click.group()
def cli():
    pass


@cli.command()
def version():
    """Shows version information."""
    click.secho('\n⚙️  linelib v2 CLI', fg="green")
    click.echo(f'{sys.version}\n\n• CLI Version: 0.1\n• Run \'py linelib\' for command help.\n')
    click.echo('- Created by AWeirdScratcher (AWeirdDev)\n')

@cli.command()
@click.option('-project', '--project', '-p', '--p', required=True)
def create(project: str):
    """
    Create a directory with Linelib examples.
    """
    if not project in AVAILABLE_EXAMPLES:
        return click.secho(f'\n\nThe example project name \'{project}\' is not available, or has been removed.\n\n', fg="red")
    click.echo('\n\nCloning example \'' + project + '\'...\n\n  • Session started.')

    fetched: list = []

    start: float = time.time()
    try:
        for url in AVAILABLE_EXAMPLES[project]:
            r = requests.get(url)
            fetched.append(r.text)
    except Exception as err:
        sN = '\n'
        click.secho('  \nFailed while fetching:', fg="yellow")
        click.echo(f'  {str(err).replace(sN, sN + "  ")}')
        click.secho('\nFailed to fetch the project. See above for more information.\n\n', fg="red")
        return False
    
    FOLDER: str = "linelib-" + str(uuid.uuid4()).split('-')[0]

    click.echo('  • Fetch complete.')
    click.echo(f'  • Appending files... ({len(FILE_NAMES[project])})')
    os.mkdir(FOLDER)

    current = 0

    for file in FILE_NAMES[project]:
        with open(FOLDER + "/" + file, "a") as f:
            f.write(fetched[current])
            f.close()
        current += 1

    end: float = time.time()
    click.echo(f'\n  → Execution Completed! (Time used: {round((end - start) * 1000)}ms)')
    click.secho(f'\n\n  Folder name: {FOLDER}', fg="blue")
    click.secho('\nDone. (100%)\n\n', fg="green")

@cli.command()
def start():
    """
    Start the development server.
    """
    click.secho('\n\nlinelib - v2', fg="green")
    click.echo('  • Starting development server...\n')

    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def web_application(path):
        return "<center>\n<h1 style=\"font-family: sans-serif; font-size: 3rem;\">Hello, World!</h1>\n<p>Specified path: /" + path + "</p>\n</center>"
    
    @app.before_first_request
    def first_req():
        click.secho('\n  • Caught: first request.\n', fg="blue")

    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    cli()