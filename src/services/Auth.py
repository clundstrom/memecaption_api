import hashlib, hmac
import os
from subprocess import Popen, PIPE


def validate(request):
    try:

        expected_hash = request.headers.get('X-Hub-Signature').replace("sha1=", "")

        calculated_hash = hmac.new(os.environ.get('WEBHOOK_KEY', '').encode("utf-8"), msg=request.data,
                                   digestmod=hashlib.sha1).hexdigest()

        is_allowed = hmac.compare_digest(calculated_hash, expected_hash)
        is_master = (request.json['ref'] == 'refs/heads/master')

        if is_allowed and is_master:
            exitcode, out, err = get_exitcode_stdout_stderr(os.environ.get('REPO'))
            if exitcode == 1:
                return 'Server error: ' + str(err), 500
            else:
                res = {"OK": out, "exitcode": exitcode, "error": err}
                return res, 200
        return f'Bad request: Allowed {is_allowed}, Master: {is_master}', 400

    except Exception as e:
        return 'Forbidden', 403


def get_exitcode_stdout_stderr(script_path):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    proc = Popen(script_path, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = proc.communicate()
    exitcode = proc.returncode

    return exitcode, out, err
