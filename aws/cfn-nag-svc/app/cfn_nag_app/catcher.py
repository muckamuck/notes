import os #noqa
import uuid #noqa
import json
from flask import Flask
from flask import request
from utility import execute_command

# str(uuid.uuid4())
app = Flask(__name__)


def allowed_file(file_name):
    if file_name:
        return True
    else:
        return False


@app.route('/', methods=['GET'])
def get_slash():
    print('get_slash() called')
    try:
        if request.method == 'GET':
            return (
                success_html,
                200,
                {'Content-Type': 'text/html'}
            )
    except Exception as wtf:
        print('upload_file() exploded: {}'.format(wtf))


@app.route('/scan', methods=['POST'])
def upload_file():
    print('upload_file() called')
    try:
        if request.method == 'POST':
            answer = scan_file(request.data)
            return (
                json.dumps(answer),
                201,
                {'Content-Type': 'text/plain'}
            )
    except Exception as wtf:
        print('upload_file() exploded: {}'.format(wtf))


def scan_file(template_contents):
    print('scan_file() called')
    temp_file_name = '/tmp/{}'.format(uuid.uuid4())
    answer = {}
    try:
        with open(temp_file_name, 'wb') as template_file:
            template_file.write(template_contents)
        command = ['/usr/local/bin/cfn_nag_scan', '--input-path', temp_file_name, '-o', 'json']
        r, stdout, stderr = execute_command(command)
        work = json.loads(stdout)
        answer['answer'] = work
        answer['exit_status'] = r
        print('execute_command - r: {}'.format(r))
        print('execute_command - stdout: {}'.format(stdout))
        print('execute_command - stderr: {}'.format(stderr))
        print('execute_command - answer: {}'.format(json.dumps(answer, indent=2)))
    except Exception as wtf:
        print('scan_file() exploded: {}'.format(wtf))
        answer['exit_status'] = -1
        answer['answer'] = str(wtf)
    finally:
        try:
            os.remove(temp_file_name)
        except:
            pass

    return answer

success_html = '''<html>
    <head><title>The Title</title></head>
    <body>
        <strong>Success</strong><br>
    </body>
</html>
'''
if __name__ == '__main__':
    app.run(debug=True)
