import sys
import subprocess
import traceback


def execute_command(self, command):
    stdout_buf = str()
    stderr_buf = str()
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        out, err = p.communicate()

        if out:
            for c in out:
                stdout_buf = stdout_buf + c

        if err:
            for c in err:
                stderr_buf = stderr_buf + c

        return p.returncode, stdout_buf, stderr_buf
    except subprocess.CalledProcessError as x:
        print('Exception caught in execute_command(): {}'.format(x))
        traceback.print_exc(file=sys.stdout)
        return x.returncode, None, None
