import json
import requests

from models.MemeTemplate import MemeTemplate
from services.MemeService import MemeService

with open('test.json') as json_file1:
    memes = json.load(json_file1)


filename = 4
for meme in memes['data']['memes']:
    path = 'D:\source\\repos\\api_tutorial\static\\'
    url = f"{meme['url']}"
    myfile = requests.get(url)
    open(path +f'{filename}.jpg', 'wb').write(myfile.content)
    filename = filename + 1
    meme = MemeTemplate(meme['name'], meme['url'], filename)
    #parse to meme template


MemeService.save(memes)