#!/usr/bin/env python3
# chip_printer.py
#
import logging
import math
import re
from PIL import ImageFont, ImageDraw, Image
from .chip import Chip

log = logging.getLogger(__name__)

class ChipPrinter:
    config = {
        'dpi': 300,
        'fontSize': DEFAULT_FONT_SIZE, # desired font size in mm but not really, font size is not an exact science
        'indentSize': 1.0,  # in mm
        'padding': 2, # pixels between edge and label
        'invert': False,
        'font': ''
    }

    _chip = None
    _font = None

    _invertRegex = re.compile(r"~[^~]*~?")

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

    def _get_pin_info(self, pin):
        pinName = self._chip[pin]
        invertRange = None

        # / and ! inverts the full pin label
        # /ABC = A̅B̅C̅
        # !DEF = D̅E̅F̅
        if pinName[0] in ('/', '!'):
            pinName = pinName[1:]
            invertRange = (0, len(pinName))
        # ~ denotes a partial invert. The first ~ starts the range and the seconds ends it.
        # If only one ~ is found, the inversion continues until the end of the label.
        # ~ABC = A̅B̅C̅  (same behavior as /ABC or !ABC)
        # A/~BC = A/B̅C̅ (continues until the end of the label)
        # a~BC~de = aB̅C̅de (range)
        else:
            result = self._invertRegex.search(pinName)
            if result:
                invertRange = result.span()
                markers = result.group() # starts with ~ and (sometimes) ends with ~
                cleanedMarkers = markers.replace('~', '') # Get rid of them
                # Check how many we want to remove (1-2) and adjust end range
                cleanedCount = len(markers) - len(cleanedMarkers)
                invertRange = (invertRange[0], invertRange[1] - cleanedCount)
                # Remove the ~ from the pin name
                pinName = pinName.replace(markers, cleanedMarkers)

        return pinName, invertRange

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
                pinName, invertRange = self._get_pin_info(pin)
                pin += 1
                textSizeX, textSizeY = draw.textsize(pinName, font=self._font)
                offsetY = math.ceil(textSizeY / 2.0)
                x = padding if effective_col == 0 else width-textSizeX-padding
                draw.text((x, y-offsetY), pinName, font=self._font)
                if invertRange:
                    charWidth = textSizeX / len(pinName)
                    xStart = x + (invertRange[0] * charWidth)
                    xEnd = x + (invertRange[1] * charWidth)
                    draw.line([(xStart,y-offsetY), (xEnd, y-offsetY)])

    def _get_indent_size(self):
        return self._mm_to_pixel(self.config['indentSize'])

    def _get_pin_row_y(self, row):
        return self._mm_to_pixel(self._chip.config['pinSpacing'] * (row + 0.5))

    def _get_font_size(self):
        return self._mm_to_pixel(self.config['fontSize'])

    def _inch_to_pixels(self, inch):
        return math.ceil(inch * self.dpi)

    def _mm_to_pixel(self, mm):
        return math.ceil(mm * self.dpi / 25.4)

    @property
    def dpi(self):
        return self.config.get('dpi', 300)

    @property
    def font(self):
        return self._font

    def get_chip_size(self, chip):
        width = self._mm_to_pixel(chip.config['rowSpacing'])
        height = self._mm_to_pixel(len(chip)//2 * chip.config['pinSpacing'])
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

    def print_chip_to_file(self, chip, output_file):
        image = self.print_chip(chip)
        image.save(output_file, dpi=(self.dpi, self.dpi))
        log.info('Output saved to %s', output_file)        
