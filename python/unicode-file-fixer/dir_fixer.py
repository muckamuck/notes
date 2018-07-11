import os
import fileinput
import string


'''
https://www.pythoncentral.io/how-to-traverse-a-directory-tree-in-python-guide-to-os-walk/
https://www.tutorialspoint.com/python/os_rename.htm
https://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
https://docs.python.org/2/library/string.html
'''


def walk_tree(start_dir):
    # Set the directory you want to start from
    rootDir = start_dir
    for dirName, subdirList, fileList in os.walk(unicode(rootDir)):
        if False:
            print('directory: {}'.format(dirName))

        if True:
            for fname in fileList:
                new_name = fix_name(fname)
                if new_name:
                    print(type(fname))
                    print(fname.encode('utf-8'))
                    print('file (bad): {}/{} => {}/{}'.format(dirName, fname.encode('utf-8'), dirName, new_name))
                    os.rename('{}/{}'.format(dirName, fname.encode('utf-8')), '{}/{}'.format(dirName, new_name))


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


def _walk_stdin():
    for d in fileinput.input():
        print(d)


def walk_stdin():
    for _d in fileinput.input():
        d = _d.strip()
        process_leaf(d)
        # print('dir: {} - {}'.format(d, leaf))


def process_leaf(d):
    parts = d.split('/')
    leaf = parts[len(parts) - 1]
    new_leaf_name = fix_name(leaf)

    if new_leaf_name:
        new_name = recreate_dir_name(parts, new_leaf_name)
        print('{} => {}'.format(d, new_name))
        # print('{} => {}'.format(d.encode('utf-8'), new_name.encode('utf-8')))
        os.rename(d, new_name)

    return True


def recreate_dir_name(parts, new_leaf_name):
    parts[-1] = new_leaf_name
    return '/'.join(parts)


def process_file(f):
    for c in f:
        print(c)

if __name__ == '__main__':
    walk_stdin()
