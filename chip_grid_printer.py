#!/usr/bin/env python3
# chip_grid_printer.py
#
from PIL import Image
import logging
import math
import operator

log = logging.getLogger(__name__)

class ChipGridPrinter:
    config = {}

    _curr_page_image = None
    _curr_page = 0
    _row_height = 0
    _page_size_pixels = None
    _padding_pixels = None

    def __init__(self, **kwargs):
        log.debug('ChipGridPrinter()')
        if kwargs:
            self.config = {**self.config, **kwargs}

        dpi = self.config['dpi']
        page_size = self.config['page_size']

        self._page_size_pixels = (self._to_pixels(page_size[0]), self._to_pixels(page_size[1]))
        log.debug('page_size_pixels: %s', self._page_size_pixels)

        self._padding_pixels = self._to_pixels(self.config['page_padding'])
        log.debug('padding_pixels: %s', self._padding_pixels)

    def new_page(self):
        self._row_height = 0
        self._curr_page += 1
        log.debug('new_page: %d', self._curr_page)
        self._curr_page_image = Image.new(mode='1', size=self._page_size_pixels, color=255)

    def save_page(self):
        image_file_name = f'page{self._curr_page}.png'
        log.debug('save page: %s', image_file_name)
        dpi =  self.config['dpi']
        self._curr_page_image.save(image_file_name, dpi=(dpi, dpi))    

    def _to_pixels(self, inch):
        return math.ceil(inch * self.config['dpi'])

    def print_chips(self, chip_printer, chip_list):
        sizedChips = [(chip, chip_printer.get_chip_size(chip)) for chip in chip_list]
        sizedChips.sort(key=operator.itemgetter(1), reverse=True)
    
        self.new_page()
        self._page_pos = (0, 0)

        for chip, chip_size in sizedChips:
            self.print_to_page(chip_printer, chip)
        self.save_page()

    def print_to_page(self, chip_printer, chip):
        chip_image = chip_printer.print_chip(chip)
        chip_size = (chip_image.size[0], chip_image.size[1])

        self._row_height = max(self._row_height, chip_size[1])

        # X overflow
        if self._page_pos[0]+chip_size[0] > self._page_size_pixels[0]:
            log.debug('new row')
            self._page_pos = (0, self._page_pos[1] + self._row_height + self._padding_pixels)
            self._row_height = chip_size[1]
        
        # Y overflow
        if self._page_pos[1]+chip_size[1] > self._page_size_pixels[1]:
            log.debug('new page')
            self._page_pos = (0, 0)
            self.save_page()
            self.new_page()

        self._curr_page_image.paste(chip_image, box=self._page_pos)

        self._page_pos = (self._page_pos[0] + chip_size[0] + self._padding_pixels, self._page_pos[1])
