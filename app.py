#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

from flask import Flask, request, abort, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from random import randint
from werkzeug.utils import secure_filename
from models.MemeRequest import MemeRequest
from services.MemeService import MemeService
from models.TextBox import TextBox
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# load credentials to memory
with open('credentials.json') as json_file:
    creds = json.load(json_file)

MEME_CACHE = []
DOGFACT_CACHE = []



def create_app():
    tmp_app = Flask(__name__)
    tmp_app.config['UPLOAD_FOLDER'] = 'static'
    tmp_app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    return tmp_app


app = create_app()
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["50 per day", "10 per hour"]
)


@app.route('/')
def hello_world():
    return {'api_online': 'true',
            'last_online': datetime.now()}


@app.route('/status')
def status():
    return {'api_online': 'true',
            'last_online': datetime.now()}


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        # template = MemeTemplate(request.form.get('name'), )

        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        # todo: createTemplate and add to db

        return redirect(
            f"http://localhost:5000/homebrew?id={request.form.get('id')}&upper={request.form.get('upper')}&lower={request.form.get('lower')}")


@app.route('/templates', methods=['GET'])
@limiter.limit("10/hour")
def templates():
    if len(MEME_CACHE) == 0:
        MEME_CACHE.append(MemeService().getMemes())
        return render_template('templates.html', results=MEME_CACHE[0])
    else:
        return render_template('templates.html', results=MEME_CACHE[0])


@app.route('/upload', methods=['GET'])
def upload_file():
    if request.args.get('pass') == creds['token']:
        return render_template('upload.html')
    else:
        return abort(403)


@app.route('/homebrew', methods=['GET'])
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


@app.route('/routedb', methods=['POST', 'GET'])
@limiter.limit("2/day")
def reroute():
    if request.method == 'POST':
        if request.args.get('token') == creds.token:
            tmp = creds.url
            creds.url = request.args.get('ip')
            return tmp + " -> " + creds.url
        else:
            return abort(403)
    else:
        return abort(403)


@app.route('/dogfact')
def randomize():
    if len(DOGFACT_CACHE) == 0:
        with open('templates/db.json') as json_file:
            data = json.load(json_file)
            for fact in data['dogfacts']:
                DOGFACT_CACHE.append(fact)
        return DOGFACT_CACHE[randint(0, len(DOGFACT_CACHE) - 1)]
    else:
        return DOGFACT_CACHE[randint(0, len(DOGFACT_CACHE) - 1)]


def setDBURL(user, pw, url, db):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=user, pw=pw,
                                                                                                  url=url, db=db)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning


# Set up database
setDBURL(creds['user'], creds['password'], creds['url'], creds['database'])
db = SQLAlchemy(app)

if __name__ == '__main__':
    updateStatus()
    app = create_app()
    app.run(debug=False, host='0.0.0.0')
