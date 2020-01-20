import json


class MemeTemplate:
    DefaultCoordinate = 0

    """
    Class which describes a meme template for the MEME API.

    :param id = ID of meme.
    :param name = Name of meme.
    :param url = Path to file.
    :param name = Name of meme.
    :param name = Name of meme.
    

    """

    def __init__(self, name: '', url: '', id, fontsize=46):
        self.name = name
        self.url = url
        self.x = self.DefaultCoordinate
        self.y = self.DefaultCoordinate
        self.fontsize = fontsize
        self.id = id

    def getUrl(self):
        return self.url

    def getId(self):
        return self.id

    @staticmethod
    def generateID(list):
        return len(list)

    def setUrl(self, url):
        self.url = url
