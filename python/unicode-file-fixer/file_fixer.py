import os
import sys
import string


def walk_tree(start_dir):
    root_dir = start_dir
    for dir_name, subdir_list, file_list in os.walk(unicode(root_dir)): #noqa
        for file_name in file_list:
            new_name = fix_name(file_name)
            if new_name:
                print('fixing: {}/{} => {}/{}'.format(
                        dir_name.encode('utf-8'),
                        file_name.encode('utf-8'),
                        dir_name.encode('utf-8'),
                        new_name.encode('utf-8')
                    )
                )
                os.rename('{}/{}'.format(
                        dir_name.encode('utf-8'), file_name.encode('utf-8')
                    ),
                    '{}/{}'.format(dir_name.encode('utf-8'), new_name)
                )


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


if __name__ == '__main__':
    if len(sys.argv) == 2:
        walk_tree(sys.argv[1])
    else:
        print('usage: python {} <directory-to-walk>'.format(sys.argv[0]))
