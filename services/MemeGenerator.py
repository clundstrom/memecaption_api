from PIL import Image, ImageDraw, ImageFont
from typing import List
from models.TextBox import TextBox
import textwrap


class MemeGenerator:
    """
    Generates memes by anchoring a TextBox to a predefined template and returns the modified image.

    """

    MaxLines = 3
    MinFontSize = 26
    WidthFactor = 0.9
    HeightFactor = 0.9

    def generate(self, url: str, boxes: List[TextBox], fontsize: int = 46):

        """
        Generates an image and returns its url.

        :param url: Path of template used for generation.
        :param boxes: Textboxes needed for Captioning.
        :param fontsize: Specified fontsize. (Default=46)
        :return:
        """

        img = Image.open(url)
        font = ImageFont.truetype("impact.ttf", fontsize)
        draw = ImageDraw.Draw(img)

        for i in range(len(boxes)):

            wrap, adj_font = self.processBox(boxes[i], img, draw, font, fontsize)

            if i == 0:
                line_offset = 0
                for line in wrap:
                    width, height = adj_font.getsize(line)
                    anchor = self.setTextAnchor(boxes[i].x, boxes[i].y, 'upper', img, draw.textsize(line, adj_font)[0])
                    draw.text((anchor[0], anchor[1] + line_offset), line, "black", adj_font, stroke_width=2,
                              stroke_fill="white")
                    line_offset = line_offset + height
            else:
                line_offset = 0
                for line in wrap:
                    width, height = font.getsize(line)
                    anchor = self.setTextAnchor(boxes[i].x, boxes[i].y, 'lower', img, draw.textsize(line, adj_font)[0])
                    draw.text((anchor[0], anchor[1] + line_offset), line, "black", adj_font, stroke_width=2,
                              stroke_fill="white")
                    line_offset = line_offset + height

        img.save('memes/tmp.png')
        return 'memes/tmp.png'

    def processBox(self, box: TextBox, img, text, font, fontsize):
        """
        Processes textbox and defines the amount of lines in a box and their size.

        :param box: Box to be processed
        :param img: Related Image
        :param text: Text to be processed
        :param font: Font
        :param fontsize: Size
        :return: List of lines and processed font.
        """

        wrap = textwrap.wrap(box.text, 23)

        if len(wrap) > self.MaxLines:
            raise InterruptedError("Too many lines.")

        while text.textsize(box.text, font)[0] > img.size[0] * self.WidthFactor \
                and fontsize > self.MinFontSize:  # Reduce fontsize if width exceeded.

            fontsize = fontsize - 1
            if fontsize < self.MinFontSize:
                fontsize = self.MinFontSize
            font = ImageFont.truetype("impact.ttf", fontsize)  # Reduce fontsize

        return wrap, font

    def setTextAnchor(self, x_offset, y_offset, boxposition, img, textsize):
        """
        Determines the correct Anchor Position of a box.

        :param x_offset: Amount of pixels left/right  -/+
        :param y_offset: Amount of pixels up/down  -/+
        :param boxposition: Upper/Lower
        :param img: Image
        :param textsize: Size of text.
        :return: [x,y] coordinates in pixels.
        """
        if boxposition == 'upper':
            x = ((img.size[0] / 2)) - ((textsize / 2)) + x_offset
            y = img.size[1] * 0.01 + y_offset
            return [x, y]
        else:
            x = ((img.size[0] / 2)) - ((textsize / 2)) + x_offset
            y = img.size[1] * self.HeightFactor + y_offset
            return [x, y]
