import hashlib, hmac
import os


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
            os.system('/home/pi/server/PortfolioAng/deploy.sh')
            return "OK", 200

        return f'Bad request: Allowed: {is_allowed}, Master: {is_master}', 400

    except Exception as e:
        return 'Forbidden', 403