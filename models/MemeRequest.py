from typing import List
from models.TextBox import TextBox


class MemeRequest:

    """
    Represents a request which is used in Processing.

    :param boxes TextBoxes that will be used with the meme template.

    """

    def __init__(self, id: int, text):
        self.text = text
        self.id = id
        self.boxes = []
        if id is None or text is None:
            raise NotImplementedError

    def getText(self):
        return self.text

    def isValidRequest(self):
        return self.boxes is not None and len(self.boxes) <= 2

    def addBox(self, box: TextBox):
        self.boxes.append(box)
