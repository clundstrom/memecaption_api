import json

from flask import send_file

from models.MemeRequest import MemeRequest
from models.MemeTemplate import MemeTemplate
from services.MemeGenerator import MemeGenerator


class MemeService:
    # list of stored templates
    StoredMemesUrl = 'templates/db.json'

    data = {'memes': []}

    def __init__(self):
        self.load()

    def process(self, memereq: MemeRequest):
        if self.validate(memereq) is False:
            return 'Invalid template ID.'

        for box in memereq.boxes:
            print(box)

        try:
            url = MemeGenerator().generate(f'templates/{memereq.id}.jpg', memereq.boxes, 46)
        except InterruptedError:
            return 'Your text was too long. Max length=69 characters'

        return send_file(url, mimetype='image/png')

    def uploadTemplate(self, template: MemeTemplate):

        # check if file exist
        # fetch new id number

        pass

    def save(self, object):
        with open('templates/db.json', 'w') as outfile:
            json.dump(object, outfile, indent=4, sort_keys=True)

    def load(self):
        with open(self.StoredMemesUrl) as json_file:
            self.data = json.load(json_file)
            print(self.data)

    def validate(self, memerequest: MemeRequest):
        for template in self.data['memes']:
            if template['id'] == str(memerequest.id):
                return True
        return False
