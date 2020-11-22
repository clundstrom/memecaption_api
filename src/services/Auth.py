import hashlib, hmac
import os
from subprocess import Popen, PIPE


def validate(request):
    try:

        expectedHash = request.headers.get('X-Hub-Signature').replace("sha1=", "")

        calculatedHash = hmac.new(os.environ.get('WEBHOOK_KEY','').encode("utf-8"), msg=request.data, digestmod=hashlib.sha1).hexdigest()

        isAllowed = hmac.compare_digest(calculatedHash, expectedHash)
        isMaster = (request.json['ref'] == 'refs/heads/master')

        if isAllowed and isMaster:
            exitcode, out, err = get_exitcode_stdout_stderr(os.environ.get('REPO'))
            if exitcode == 1:
                return 'Server error: ' + str(err), 500
            else:
                return 'OK', 200
        return f'Bad request: Allowed {isAllowed}, Master: {isMaster}', 400

    except Exception as e:
        return 'Forbidden', 403


def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = proc.communicate()
    exitcode = proc.returncode

    return exitcode, out, err
