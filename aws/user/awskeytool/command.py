import sys
import click
import platform

valid_systems = [
    'linux',
    'darwin'
]


@click.group()
@click.version_option(version='0.5.3')
def cli():
    pass


@cli.command()
@click.option('--user-name', '-u', help='user name of interest', required=True)
@click.option('--profile', '-p', help='profile of interest', required=True)
def rotate(user_name):
    print('Rotating keys for {}'.format(user_name))


def verify_real_system():
    try:
        current_system = platform.system().lower()
        return current_system in valid_systems
    except:
        return False

if not verify_real_system():
    print('error: unsupported system')
    sys.exit(1)
