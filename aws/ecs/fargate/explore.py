import json
import sys


def explore(template_file):
    '''
    Explore the resource that might be created by a CloudFormation template.

    Args:
        template_file - the JSON cloud formation template

    Returns:
        True if happy else False
    '''
    try:
        with open(template_file) as f:
            t = json.load(f)
            for k in t['Resources']:
                print('{} - {}'.format(k, t['Resources'][k]['Type']))
        return True
    except Exception as wtf:
        print('explore() blew up: {}'.format(wtf))
        return False


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if explore(sys.argv[1]):
            sys.exit(0)
    else:
        print('usage: python {} <template-file>'.format(sys.argv[0]))

    sys.exit(1)
