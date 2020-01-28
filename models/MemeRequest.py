from typing import List
from models.TextBox import TextBox


class MemeRequest:
    """
    Represents a request which is used in Processing.

    :param boxes TextBoxes that will be used with the meme template.

    """

    def __init__(self, id: int, text, x_offset=0, y_offset=0):
        self.text = text
        self.id = id
        self.boxes = []
        self.x_offset = x_offset
        self.y_offset = y_offset
        if self.id is None or text is None:
            raise NotImplementedError

    def getText(self):
        return self.text

    def isValidRequest(self):
        return self.boxes is not None and len(self.boxes) <= 2

    def addBox(self, box: TextBox):
        self.boxes.append(box)
