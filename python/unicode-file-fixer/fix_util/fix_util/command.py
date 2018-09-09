import os
import sys
import click
import fileinput #noqa
import string
from shutil import copyfile

verbos = False


@click.group()
@click.version_option(version='0.0.1')
def cli():
    pass


@cli.command()
@click.option('--work-dir', '-w', help='Target directory for fixed files', required=True)
@click.option('--dryrun', '-d', help='dry run', is_flag=True)
def fix(work_dir, dryrun):
    try:
        walk_stdin(work_dir, dryrun)
        sys.exit(0)
    except Exception as wtf:
        print('fix() exploded: {}'.format(wtf))
        sys.exit(1)


def walk_stdin(work_dir, dryrun):
    for _thing in sys.stdin:
        thing = _thing.strip()
        process_file(work_dir, thing, dryrun)


def fix_name(_file_name):
    file_name = list(_file_name)
    fixed = False
    count = len(file_name)
    idx = 0
    while idx < count:
        c = file_name[idx]
        if c not in string.printable:
            file_name[idx] = '_'
            fixed = True
        idx = idx + 1

    if fixed:
        return ''.join(file_name)
    else:
        return None


def process_file(work_dir, path_name, dryrun):
    try:
        new_name = fix_name(path_name)
        if not new_name:
            if dryrun and verbos:
                print('(dryrun) [good] {}'.format(path_name))
            return

        parts = path_name.split('/')
        parts = new_name.split('/')
        d = '/'.join(parts[:-1])
        f = parts[-1] #noqa
        target_dir = '{}/{}'.format(work_dir, d)
        target_file = '{}/{}'.format(work_dir, new_name)
        try:
            if not dryrun:
                os.makedirs(target_dir)
        except:
            pass

        if False:
            sz = os.path.getsize(path_name)
            print('SIZE: {}'.format(sz))
            print('SRC[{}]: {}'.format(type(path_name), path_name))
            print('DST[{}]: {}'.format(type(target_file), target_file))
            print()
        else:
            if dryrun:
                sz = os.path.getsize(path_name)
                print('(dryrun) [{}] {}'.format(sz, path_name))
            else:
                copyfile(path_name, target_file)
                print('Fixed: {}'.format(target_file))

    except Exception as wtf:
        print(str(wtf))


def process_leaf(d):
    parts = d.split('/')
    leaf = parts[len(parts) - 1]
    new_leaf_name = fix_name(leaf)

    if new_leaf_name:
        new_name = recreate_dir_name(parts, new_leaf_name)
        print('{} => {}'.format(d, new_name))
        os.rename(d, new_name)

    return True


def recreate_dir_name(parts, new_leaf_name):
    parts[-1] = new_leaf_name
    return '/'.join(parts)
