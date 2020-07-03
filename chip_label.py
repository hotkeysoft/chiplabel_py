#!/usr/bin/env python3
from args import parse_args
from chip import Chip
from chip_list import ChipList
from chip_printer import ChipPrinter
from chip_grid_printer import ChipGridPrinter
import logging
from PIL import Image
log = logging.getLogger()

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
    config['page_size'] = args.page_size
    config['page_padding'] = args.page_padding

    printer = ChipPrinter(**config)

    if not args.page:
        for chip in chip_list:
            log.info('Generating label for chip: %s', chip.id)
            #TODO: Prefix lib name flag
            output_file = f"{output_dir}{chip.unscoped_id}.png"
            printer.print_chip_to_file(chip, output_file)
    else:
        gridPrinter = ChipGridPrinter(**config)
        gridPrinter.print_chips(printer, chip_list)

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
