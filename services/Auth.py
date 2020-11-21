import hashlib, hmac
import os
import json
import shlex
from subprocess import Popen, PIPE


def validate(data):
    try:
        parsed = json.load(data)

        expectedHash = parsed['X-Hub-Signature'].replace("sha=1", "")
        calculatedHash = hmac.new(bytes(os.environ.get('WEBHOOK_KEY')), data, hashlib.sha1).hexdigest()

        isAllowed = hmac.compare_digest(calculatedHash, expectedHash)
        isMaster = (parsed['ref'] == 'refs/heads/master')
        cmd = "cd " + os.environ.get('REPO') + " && " + "/deploy.sh"

        if isAllowed and isMaster:
            exitcode, out, err = get_exitcode_stdout_stderr(cmd)
            if exitcode == 1:
                return 400, 'Bad request: ' + str(err)
            else:
                return 200, 'OK'

    except Exception as e:
        return 403, 'Forbidden'


def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    return exitcode, out, err
