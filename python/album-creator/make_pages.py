from string import Template
import os #noqa
import fileinput
from page_html import html


def walk_stdin():
    work_list = []
    for _f in fileinput.input():
        f = _f.strip()
        parts = f.split('.')
        parts.pop(-1)
        f = ''.join(parts)
        stub_name = '{}'.format(f.replace('/', '_'))
        html_name = '{}.html'.format(f.replace('/', '_'))
        big_name = 'full/{}.JPG'.format(f)
        small_name = 'web/{}.JPG'.format(f)
        wrk = {
            'html': html_name,
            'big_name': big_name,
            'small_name': small_name,
            'stub_name': stub_name
        }
        work_list.append(wrk)

    return work_list


def process_list(work_list):
    idx = 0

    t = Template(html)
    while idx < len(work_list):
        prev_idx = idx - 1
        next_idx = idx + 1
        if next_idx >= len(work_list):
            next_idx = 0

        prev_thing = work_list[prev_idx]
        this_thing = work_list[idx]
        next_thing = work_list[next_idx]
        if True:
            buf = t.substitute(
                bigImage=this_thing.get('big_name', None),
                smallImage=this_thing.get('small_name', None),
                stub=this_thing.get('stub_name', None),
                prevHtml=prev_thing.get('html', None),
                nextHtml=next_thing.get('html', None)
            )
            print(buf)
        else:
            print(this_thing.get('big_name', 'unknown'))
            print(this_thing.get('small_name', None))
            print(prev_thing.get('html', None))
            print(next_thing.get('html', None))

        html_file_name = '../{}'.format(this_thing.get('html', None))
        print(html_file_name)
        write_page(html_file_name, buf)
        if idx == 0:
            write_page('../index.html', buf)

        print('==================================================================')
        idx = idx + 1
    return True


def write_page(file_name, buf):
    try:
        with open(file_name, 'w') as page:
            page.write(buf)
    except Exception as wtf:
        print(wtf)


def recreate_dir_name(parts, new_leaf_name):
    parts[-1] = new_leaf_name
    return '/'.join(parts)


if __name__ == '__main__':
    work_list = walk_stdin()
    process_list(work_list)
