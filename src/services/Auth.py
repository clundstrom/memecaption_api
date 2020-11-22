import hashlib, hmac
import os
import shlex
from subprocess import Popen, PIPE


def validate(request):
    """
    Validates webhook request by comparing hashes of the request data
    with a hmac key. Triggers a deploy script on the backend.
    :param request:
    :return:
    """
    try:

        expected_hash = request.headers.get('X-Hub-Signature').replace("sha1=", "")

        calculated_hash = hmac.new(os.environ.get('WEBHOOK_KEY', '').encode("utf-8"), msg=request.data,
                                   digestmod=hashlib.sha1).hexdigest()

        is_allowed = hmac.compare_digest(calculated_hash, expected_hash)
        is_master = (request.json['ref'] == 'refs/heads/master')

        if is_allowed and is_master:
            exitcode, out, err = get_exitcode_stdout_stderr("bash " + str(os.environ.get('REPO')))
            if exitcode == 1:
                return 'Server error: ' + str(err), 500
            else:
                res = {"OK": str(out), "exitcode": str(exitcode), "error": str(err)}
                return res, 200
        return f'Bad request: Allowed {is_allowed}, Master: {is_master}', 400

    except Exception as e:
        return 'Forbidden', 403


def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode

    return exitcode, out, err
