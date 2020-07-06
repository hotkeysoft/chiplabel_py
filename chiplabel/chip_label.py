#!/usr/bin/env python3

import logging
import os
from PIL import Image
from .args import parse_args
from .chip import Chip
from .chip_list import ChipList
from .chip_printer import ChipPrinter
from .chip_grid_printer import ChipGridPrinter

log = logging.getLogger()

def _to_chip_list(chip_list, chip_ids):
    chips = []
    for chip_id in chip_ids:
        chip = chip_list[chip_id]
        if not chip:
            log.warning('Chip not found: %s, skipping', chip_id)
        else:
            chips.append(chip)
    return chips

def print_chips_text(chip_list, args):
    log.info('Printing %s chips to text', len(chip_list))
    for chip in chip_list:
        print()
        chip.print_ASCII()

def print_chips_image(chip_list, args):
    if not os.path.isdir(args.output):
        log.error('Output directory not found [%s]', args.output)
        return

    log.info('Printing %s chips to .png', len(chip_list))
    output_dir = args.output
    if output_dir[-1] not in ('/', '\\'):
        output_dir = output_dir + '/'

    config = vars(args)
    log.debug('config: %s', config)

    if not args.page:
        chip_printer = ChipPrinter(**config)
        for chip in chip_list:
            log.info('Generating label for chip [%s]', chip.id)
            #TODO: Prefix lib name flag
            output_file = f"{output_dir}{chip.unscoped_id}.png"
            chip_printer.print_chip_to_file(chip, output_file)
    else:
        #TODO: Output directory/file pattern
        gridPrinter = ChipGridPrinter(**config)
        gridPrinter.print_chips(chip_list)

class LogFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            self._style._fmt = "%(message)s"
        else:
            self._style._fmt = "%(levelname)s: %(message)s"
        return super().format(record)

def main(argv):
    args = parse_args(argv[1:])

    # Configure logging
    old_loglevel = log.level
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter())
    log.setLevel(args.loglevel)
    log.addHandler(handler)

    try:
        chip_list = ChipList()
        try:
            chip_list.load(args.input)
        except IOError as ex:
            log.error('Error loading chip list [%s]: %s', args.input, ex)
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
                out_of = f'(out of {len(args.chip)})' if len(chips) != len(args.chip) else ''
                log.info('Found %d chips %s', len(chips), out_of)
                print_chips(chips, args)
            else: 
                log.warning('Nothing to do')
    finally:
        # Reset log in case we're not running as a standalong app
        log.removeHandler(handler)
        log.setLevel(old_loglevel)

if __name__ == '__main__':
    import sys
    MIN_PYTHON = (3, 6)
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)
    main(sys.argv)
