class TextBox(object):
    """
    Class to define the TextBox used in a MemeRequest.
    :param x,y Takes pixel-based coordinates.
    :param text Text contained by box.

    """

    def __init__(self, text: str, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
        self.text = text

    def isTextValid(self):
        return self.text is None

    def setText(self, text):
        self.text = text

    def __str__(self):
        return f'(X: {self.x}, Y: {self.y} : {self.text})'
