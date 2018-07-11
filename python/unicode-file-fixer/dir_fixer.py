import os
import fileinput
import string


'''
https://www.pythoncentral.io/how-to-traverse-a-directory-tree-in-python-guide-to-os-walk/
https://www.tutorialspoint.com/python/os_rename.htm
https://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
https://docs.python.org/2/library/string.html
'''


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


def walk_stdin():
    for _d in fileinput.input():
        d = _d.strip()
        process_leaf(d)


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


if __name__ == '__main__':
    walk_stdin()
