from flask import Blueprint
from src.services import Auth
import json
from datetime import datetime
from flask import request, abort, render_template, make_response
from random import randint
from src.modules.Memes.MemeRequest import MemeRequest
from src.services.MemeService import MemeService
from src.modules.Memes.TextBox import TextBox
from api_setup import limiter
from src.modules.Cipher import crypto
import re

# Caches
MEME_CACHE = []
DOGFACT_CACHE = []

open_routes = Blueprint('open_routes', __name__)


@open_routes.route('/')
def entrypoint():
    return {'api_online': 'true',
            'last_online': datetime.now()}


@open_routes.route('/templates', methods=['GET'])
@limiter.limit("10/hour")
def templates():
    if len(MEME_CACHE) == 0:
        MEME_CACHE.append(MemeService().getMemes())
        return render_template('templates.html', results=MEME_CACHE[0], timeout=0.5)
    else:
        return render_template('templates.html', results=MEME_CACHE[0], timeout=0.5)


@open_routes.route('/hook', methods=['POST'])
def hook():
    if request:
        if request.data:
            response = Auth.validate(request)
            return make_response(response)
        else:
            return abort(403)


@open_routes.route('/cipher', methods=['GET'])
def caesar_cipher():
    try:
        if request.args:
            ciphertext: str = request.args.get('text')
            sanitized = re.sub(r"[^A-za-z]+", "", ciphertext)
            keys = crypto.chi_key_search(sanitized)
            result = min(keys, key=lambda t: t[1])

            res = {"shift_key": result[0], "chi": result[1], "decipher": result[2]}
            return make_response(res, 200)
        else:
            return abort(400)

    except Exception as e:
        return abort(400)


@open_routes.route('/homebrew', methods=['GET'])
def generateMeme():
    try:
        # Create Request
        memereq = MemeRequest(request.args.get('id'), request.args.get('upper'))
        x1_offset = 0
        y1_offset = 0

        #  Check passed arguments
        if request.args.get('x') is not None:
            x1_offset = int(request.args.get('x'))

        if request.args.get('y') is not None:
            y1_offset = int(request.args.get('y'))

        if request.args.get('upper') is not None:
            upper = TextBox(request.args.get('upper'), x1_offset, y1_offset)
            memereq.addBox(upper)

        if request.args.get('lower') is not None:
            lower = TextBox(request.args.get('lower'), 0, 0)
            memereq.addBox(lower)

        # Process meme if valid
        if memereq.isValidRequest():
            url = MemeService().process(memereq)
        else:
            url = 'invalid arguments'

    except NotImplementedError:
        return abort(401)

    return url


@open_routes.route('/dogfact')
def randomize():
    if len(DOGFACT_CACHE) == 0:
        with open('templates/db.json') as json_file:
            data = json.load(json_file)
            for fact in data['dogfacts']:
                DOGFACT_CACHE.append(fact)
        return DOGFACT_CACHE[randint(0, len(DOGFACT_CACHE) - 1)]
    else:
        return DOGFACT_CACHE[randint(0, len(DOGFACT_CACHE) - 1)]  # return cached facts
