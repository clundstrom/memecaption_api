import json
import jsonpickle
import requests
from src.modules.Memes.MemeTemplate import MemeTemplate
from src.services.MemeService import MemeService

"""
Script used to download meme templates from a specified source.

"""

db = MemeService().load()

with open('test.json') as json_file1:
    memes = json.load(json_file1)

filename = 4
for meme in memes['data']['memes']:
    path = 'D:\source\\repos\\api_tutorial\\static\\'
    url = f"{meme['url']}"
    myfile = requests.get(url)
    # open(path +f'{filename}.jpg', 'wb').write(myfile.content)
    tmp = jsonpickle.encode(MemeTemplate(meme['name'], f'{filename}.jpg', filename))
    filename = filename + 1
    db['memes'].append(tmp)

# MemeService.save(db)
