#!/usr/bin/env python3
# chip_grid_printer.py
#
import logging
import math
import operator
import os
from PIL import Image
from .chip_printer import ChipPrinter

log = logging.getLogger(__name__)

class ChipGridPrinter(ChipPrinter):
    _page_pos = (0, 0)
    _curr_page_image = None
    _curr_page = 0
    _row_height = 0

    def __init__(self, **kwargs):
        log.debug('ChipGridPrinter()')
        ChipPrinter.__init__(self, **kwargs)
        self.reset()

    @property
    def page_padding(self):
        return self.config.get('page_padding', 0.1)

    @property
    def page_padding_pixels(self):
        page_padding = self.page_padding
        return self._inch_to_pixels(self.page_padding)

    @property
    def page_size(self):
        return self.config.get('page_size', (1, 1))

    @property
    def page_size_pixels(self):
        page_size = self.page_size
        return (self._inch_to_pixels(page_size[0]), self._inch_to_pixels(page_size[1]))

    @property
    def current_page(self):
        return self._curr_page

    @property
    def page_pos(self):
        return self._page_pos

    def reset(self):
        log.debug('reset()')
        self._curr_page = 0
        self.new_page()

    def new_page(self):
        self._page_pos = (0, 0)
        self._row_height = 0
        self._curr_page += 1
        log.debug('new_page: %d', self._curr_page)
        self._curr_page_image = Image.new(mode='1', size=self.page_size_pixels, color=255)

    def _crop_image(self):
        if self.config.get('page_nocrop', False):
            return
        inverted = Image.eval(self._curr_page_image, (lambda x: 1-x))
        self._curr_page_image = self._curr_page_image.crop(inverted.getbbox())        

    def _get_output_dir(self):
        output_dir = str(self.config.get('output', '.'))
        if output_dir[-1] not in ('/', '\\'):
            output_dir = output_dir + '/'
        
        if not os.path.isdir(output_dir):
            raise ValueError(f'Invalid output directory: {output_dir}')
        return output_dir

    def save_page(self):
        log.debug('save_page()')

        output_dir = self._get_output_dir()
        image_file_name = f'{output_dir}page{self._curr_page}.png'
        log.debug('save page: %s', image_file_name)
        dpi = self.dpi
        self._crop_image()
        self._curr_page_image.save(image_file_name, dpi=(dpi, dpi))    

    def print_chips(self, chip_list):
        sizedChips = [(chip, self.get_chip_size(chip)) for chip in chip_list]
        sizedChips.sort(key=operator.itemgetter(1), reverse=True)
    
        for chip, chip_size in sizedChips:
            self.print_to_page(chip)
        self.save_page()

    def print_to_page(self, chip):
        chip_image = self.print_chip(chip)
        chip_size = chip_image.size

        self._row_height = max(self._row_height, chip_size[1])

        # X overflow
        if self._page_pos[0]+chip_size[0] > self.page_size_pixels[0]:
            log.debug('new row')
            self._page_pos = (0, self._page_pos[1] + self._row_height + self.page_padding_pixels)
            self._row_height = chip_size[1]
        
        # Y overflow
        if self._page_pos[1]+chip_size[1] > self.page_size_pixels[1]:
            log.debug('new page')
            self.save_page()
            self.new_page()

        self._curr_page_image.paste(chip_image, box=self._page_pos)

        self._page_pos = (self._page_pos[0] + chip_size[0] + self.page_padding_pixels, self._page_pos[1])
