#!/usr/bin/env python3
# chip_printer.py
#
import math
from chip import Chip
from PIL import ImageFont, ImageDraw, Image
import logging
log = logging.getLogger(__name__)

class ChipPrinter:
    config = {
        'dpi': 300,
        'fontSize': 1.0, # desired font size in mm but not really, font size is not an exact science
        'indentSize': 1.0,  # in mm
        'padding': 2, # pixels between edge and label
        'invert': False,
        'font': './fonts/CascadiaMono.ttf'
    }

    _chip = None
    _font = None

    def __init__(self, **kwargs):
        if kwargs:
            self.config = {**self.config, **kwargs}

        self._init_font()

    def _init_font(self):
        font_size = self._get_font_size()
        try:
            self._font = ImageFont.truetype(self.config['font'], font_size)
        except IOError:
            log.warning(f'Unable to load font: [%s], using internal fixed size font', self.config['font'])
            self._font = ImageFont.load_default()

    def _draw_border(self, image):
        draw = ImageDraw.Draw(image)
        x,y = image.size
        draw.rectangle([(0,0), (x-1, y-1)])

    def _draw_chip_indent(self, image):
        _, canvasY = image.size
        indentPixels = self._get_indent_size()
        x0 = 0
        x1 = indentPixels
        y0 = (canvasY-indentPixels)//2
        y1 = y0 + indentPixels
        draw = ImageDraw.Draw(image)
        draw.line([(x0, y0), (x1//2, y0)])
        draw.line([(x0, y1), (x1//2, y1)])
        draw.arc([(x0, y0), (x1, y1)], 270, 90)

    def _draw_chip_name(self, image):
        _, canvasY = image.size
        draw = ImageDraw.Draw(image)
        x0 = math.ceil(self._get_indent_size() * 1.2)

        label = self._chip.full_name
        _, textSizeY = draw.textsize(label, font=self._font)
        draw.text((x0, (canvasY-textSizeY)//2), label, font=self._font)

    def _draw_pins(self, image):
        width, height = image.size
        draw = ImageDraw.Draw(image)
        padding = self.config['padding']
        rows = len(self._chip) // 2
        pin = 1
        for col in range(2):
            effective_col = 1-col if self.config['invert'] else col
            for row in range(rows):
                y = self._get_pin_row_y(row)
                if (col == 1):
                    y = height-y
                pinName = self._chip[pin]
                invert = pinName[0] in ('~', '/', '!')
                pinName = pinName[1:] if invert else pinName
                pin += 1
                textSizeX, textSizeY = draw.textsize(pinName, font=self._font)
                offsetY = math.ceil(textSizeY / 2.0)
                x = padding if effective_col == 0 else width-textSizeX-padding
                draw.text((x, y-offsetY), pinName, font=self._font)
                if invert:
                    draw.line([(x,y-offsetY), (x+textSizeX, y-offsetY)])

    def _get_indent_size(self):
        return math.ceil(self.config['indentSize'] * self.config['dpi'] / 25.4)

    def _get_pin_row_y(self, row):
        y = self._chip.config['pinSpacing'] * (row + 0.5) * self.config['dpi'] / 25.4
        return math.ceil(y)

    def _get_font_size(self):
        height = self.config['fontSize'] * self.config['dpi'] / 25.4
        return math.ceil(height)

    def get_chip_size(self, chip):
        width = chip.config['rowSpacing'] * self.config['dpi'] / 25.4
        height = (len(chip)//2) * chip.config['pinSpacing'] * self.config['dpi'] / 25.4
        return (math.ceil(width), math.ceil(height))

    def print_chip(self, chip):
        log.debug('print_chip(%s) config=%s', chip, self.config)
        self._chip = chip

        canvas_size = self.get_chip_size(chip)
        log.debug('canvas_size=%s', canvas_size)

        image = Image.new(mode='1', size=canvas_size, color=255)

        self._draw_border(image)
        self._draw_pins(image)

        rotated = image.rotate(90, expand=True)

        self._draw_chip_name(rotated)
        self._draw_chip_indent(rotated)
        return rotated

def main(args):
    logging.basicConfig(level=logging.DEBUG)

    chip = Chip('7404', 14)
    pins = [str(pin+1) for pin in range(14)]
    for pinnum, pin in enumerate(chip, 1):
        chip[pinnum] = pins[pinnum-1]

    printer = ChipPrinter()
    image = printer.print_chip(chip)
    image.save("./out.png", dpi=(printer.config['dpi'], printer.config['dpi']))

    printer_inverted = ChipPrinter(invert=True)
    image = printer_inverted.print_chip(chip)
    image.save("./out_inverted.png", dpi=(printer.config['dpi'], printer.config['dpi']))

    #test bad font
    printer_bad_font = ChipPrinter(font='')
    image = printer_bad_font.print_chip(chip)
    image.save("./out_badfont.png", dpi=(printer.config['dpi'], printer.config['dpi']))

if __name__ == '__main__':
    import sys
    main(sys.argv)
