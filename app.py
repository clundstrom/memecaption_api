#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

from flask import Flask, request, jsonify, abort, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from random import randint

from werkzeug.utils import secure_filename

from models.MemeRequest import MemeRequest
from models.MemeTemplate import MemeTemplate
from services.MemeService import MemeService
from models.TextBox import TextBox

dogfact = ['Did you know a dog\'s nose print is unique, much like person\'s fingerprint?',
           '45% of U.S dogs sleep in their owner\'s bed.',
           'All dogs dream, but puppies and senior dogs dream more frequently than adult dogs.',
           'Seventy percent of people sign their dog\'s name on their holiday cards.',
           'A dog\'s sense of smell is legendary, but did you know that his nose has as many as 300 million receptors? In comparison, a human nose has about 5 million.',
           'The shape of a dog’s face suggests its longevity: A long face means a longer life.',
           'Dogs noses are wet to help absorb scent chemicals',
           'Did you know that three dogs survived the sinking of the Titanic? Vetstreet states that the dogs were in first class and included a Pomeranian puppy - which her owner wrapped in a blanket to escape with, and everyone thought she was carrying a baby. Another Pomeranian and a Pekingese were also rescued. Move over Rose and Jack!',
           'A Greyhound would actually beat a Cheetah in a long distance race! According to Psychology Today, Greyhounds are excellent long distance runners and can keep a speed of 35mph for up to 7 miles. Where the Cheetah is incredibly fast it can only keep its speed for around 200 - 300 yards, so they may have the running start but it would soon be surpassed by a Greyhound!',
           'If you thought all dogs barked, then prepare yourself for this dog fact. The Basenji dog doesn’t tend to bark, instead they are known to yodel, whine or scream.',
           'UFAW states that on average around 30% of Dalmatians are deaf in one ear and 5% are deaf in both. This is due to something called the extreme piebald gene which is responsible for their white coat and blue eyes (in some of them). Dalmatians with larger dark patches are less likely to be deaf.',
           'Many owners haven’t heard of this interesting dog fact, but did you know that your four-legged friend has three eyelids? According to iHeartDogs, the third lid is called the \'haw\' or nictitating membrane, and it’s responsible for keeping the eye protected and lubricated.']

with open('credentials.json') as json_file:
    creds = json.load(json_file)

app = Flask(__name__)


def setDBURL(user, pw, url, db):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=user, pw=pw,
                                                                                                  url=url, db=db)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning


app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Set up database
setDBURL(creds['user'], creds['password'], creds['url'], creds['database'])
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), unique=True)
    post_text = db.Column(db.String(255))

    def __init__(self, title, post_text):
        self.title = title
        self.post_text = post_text


@app.route('/')
def hello_world():
    return '<b>Hello World!</b>'


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
def templates():
    f = []
    for (dirpath, dirnames, filenames) in os.walk('static'):
        f.extend(filenames)

    return render_template('templates.html', results=MemeService.Data)


@app.route('/upload', methods=['GET'])
def upload_file():
    if request.args.get('pass') == creds['password']:
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

        if request.args.get('lower') is not None:
            lower = TextBox(request.args.get('lower'), 0, 0)
            memereq.addBox(lower)

        upper = TextBox(request.args.get('upper'), x1_offset, y1_offset)
        memereq.addBox(upper)

        # Process meme if valid
        if memereq.isValidRequest():
            url = MemeService().process(memereq)
        else:
            url = 'invalid arguments'

    except NotImplementedError:
        return abort(401)

    return url


@app.route('/routedb', methods=['POST', 'GET'])
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
    return jsonify(dogfact[randint(0, len(dogfact) - 1)])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
