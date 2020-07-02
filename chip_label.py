#!/usr/bin/env python3
from args import parse_args
from chip import Chip
from chip_list import ChipList
from chip_printer import ChipPrinter
import logging
import math
import operator
from PIL import Image
log = logging.getLogger()

def _to_pixels(inch, dpi):
    return math.ceil(inch * dpi)

def _to_chip_list(chip_list, chip_ids):
    chips = []
    for chip_id in chip_ids:
        chip = chip_list[chip_id]
        if not chip:
            log.error('Chip not found: %s', chip_id)
            return None
        chips.append(chip)
    return chips

def print_chips_text(chip_list, args):
    log.info('Printing %s chips (text)', len(chip_list))
    for chip in chip_list:
        print()
        chip.print_ASCII()

curr_page = 0
curr_page_image = None
row_height = 0
page_size_pixels = None
padding_pixels = None
dpi = None

def print_chips_image(chip_list, args):
    log.info('Printing %s chips (image)', len(chip_list))
    output_dir = args.output
    if output_dir[-1] not in ('/', '\\'):
        output_dir = output_dir + '/'

    config = {}
    if args.font:
        config['font'] = args.font
    if args.dpi:
        config['dpi'] = args.dpi
    if args.invert:
        config['invert'] = True

    printer = ChipPrinter(**config)

    if not args.page:
        for chip in chip_list:
            log.info('Generating label for chip: %s', chip.id)
            print_chip_image(printer, chip, output_dir)
    else:
        global page_size_pixels
        page_size_pixels = (_to_pixels(args.page_size[0], args.dpi), _to_pixels(args.page_size[1], args.dpi))
        log.debug('page_size_pixels: %s', page_size_pixels)

        global padding_pixels
        padding_pixels = _to_pixels(args.page_padding, args.dpi)
        log.debug('padding_pixels: %s', padding_pixels)

        sizedChips = [(chip, printer.get_chip_size(chip)) for chip in chip_list]
        sizedChips.sort(key=operator.itemgetter(1), reverse=True)
    
        global dpi
        dpi = printer.config['dpi']

        new_page()
        page_pos = (0, 0)

        for chip, chip_size in sizedChips:
            page_pos = print_to_page(printer, page_pos, chip)

        save_page()

def new_page():
    global curr_page_image
    global curr_page    
    global row_height
    row_height = 0
    curr_page += 1
    log.debug('new_page: %d', curr_page)
    curr_page_image = Image.new(mode='1', size=page_size_pixels, color=255)

def save_page():
    global curr_page_image
    image_file_name = f'page{curr_page}.png'
    log.debug('save page: %s', image_file_name)
    curr_page_image.save(image_file_name, dpi=(dpi, dpi))

def print_to_page(printer, page_pos, chip):
    global row_height
    global curr_page_image

    chip_image = printer.print_chip(chip)
    chip_size = (chip_image.size[0], chip_image.size[1])

    row_height = max(row_height, chip_size[1])

    # X overflow
    if page_pos[0]+chip_size[0] > page_size_pixels[0]:
        log.debug('new row')
        page_pos = (0, page_pos[1] + row_height + padding_pixels)
        row_height = chip_size[1]
    
    # Y overflow
    if page_pos[1]+chip_size[1] > page_size_pixels[1]:
        log.debug('new page')
        page_pos = (0, 0)
        save_page()
        new_page()

    curr_page_image.paste(chip_image, box=page_pos)

    page_pos = (page_pos[0] + chip_size[0] + padding_pixels, page_pos[1])
    return page_pos

def print_chip_image(printer, chip, output_dir):
    image = printer.print_chip(chip)
    #TODO: Prefix lib name flag
    output_file = f"{output_dir}{chip.unscoped_id}.png"
    image.save(output_file, dpi=(printer.config['dpi'], printer.config['dpi']))
    log.info('Output saved to %s', output_file)

class LogFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            self._style._fmt = "%(message)s"
        else:
            self._style._fmt = "%(levelname)s: %(message)s"
        return super().format(record)

def main():
    args = parse_args()

    # Configure logging
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter())
    log.setLevel(args.loglevel)
    log.addHandler(handler)

    chip_list = ChipList()
    chip_list.load(args.input)
    if not len(chip_list):
        log.error('No chip loaded')
        return

    print_chips = print_chips_text if args.text else print_chips_image

    if args.list:
        for chip in sorted(chip_list.names, key=str.casefold):
            print(chip)
    elif args.all:
        print_chips(chip_list, args)
    else:
        chips = _to_chip_list(chip_list, args.chip)
        if chips and len(chips):
            print_chips(chips, args)
        else: 
            log.info('Nothing to do')

if __name__ == '__main__':
    import sys
    MIN_PYTHON = (3, 6)
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)
    main()
