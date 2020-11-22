import json
import jsonpickle
from flask import send_file
from src.modules.Memes.MemeRequest import MemeRequest
from src.services.MemeGenerator import MemeGenerator


class MemeService:
    """
    Handles processing of MemeRequests.
    """

    # List of stored templates
    StoredMemesUrl = 'templates/db.json'
    # Cached
    Data = {}
    Memes = []

    def __init__(self):
        self.load()

    def process(self, memereq: MemeRequest):
        if self.validate(memereq) is False:
            return 'Invalid template ID.'

        for box in memereq.boxes:
            print(box)

        try:
            url = MemeGenerator().generate(f'static/{memereq.id}.jpg', memereq.boxes)
        except InterruptedError:
            return 'Your text was too long. Max length=69 characters'

        return send_file(url, mimetype='image/png')

    @staticmethod
    def save(obj):
        with open('templates/db.json', 'w') as outfile:
            json.dump(obj, outfile, indent=4, sort_keys=True)

    def load(self):
        if len(self.Memes) == 0:
            with open(self.StoredMemesUrl) as json_file:
                self.Data = json.load(json_file)
                for meme in self.Data['memes']:
                    self.Memes.append(jsonpickle.decode(meme))
                return self.Memes

    def validate(self, memerequest: MemeRequest):
        for template in self.Memes:
            if template.id == int(memerequest.id):
                return True
        return False

    @classmethod
    def getMemes(self):
        return self.Memes
