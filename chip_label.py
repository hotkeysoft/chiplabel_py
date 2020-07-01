#!/usr/bin/env python3
from PIL import ImageFont, ImageDraw, Image
from chip import Chip
from chip_printer import ChipPrinter
from chip_list import ChipList
import math
import argparse
import logging
log = logging.getLogger()

MIN_DPI = 50
MAX_DPI = 2000
DEFAULT_DPI = 300

DEFAULT_FONT = './fonts/CascadiaMono.ttf'
DEFAULT_INPUT_DIR = './chips'
DEFAULT_OUTPUT_DIR = './out'

def print_chip_label(chip_list, chip_id, args):
    chip = chip_list[chip_id]
    if not chip:
        log.error('Chip not found: %s', chip_id)
        return
    log.info('Generating label for chip: %s', chip.id)

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
    image = printer.print_chip(chip)
#TODO: Prefix lib name flag
    output_file = f"{output_dir}{chip.unscoped_id}.png"
    image.save(output_file, dpi=(printer.config['dpi'], printer.config['dpi']))
    log.info('Output saved to %s', output_file)

def _dpi_range(string):
    try:
        value = int(string)
        if value < MIN_DPI or value > MAX_DPI:
            raise argparse.ArgumentTypeError(f'{value} is not in range [{MIN_DPI}, {MAX_DPI}]')
    except ValueError:
        raise argparse.ArgumentTypeError(f'{string} is not an integer value')
    return value

class LogFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            self._style._fmt = "%(message)s"
        else:
            self._style._fmt = "%(levelname)s: %(message)s"
        return super().format(record)

def parse_args():
    parser = argparse.ArgumentParser(description='Generate footprint images for chips.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-c', '--chip',
        metavar='name',
        help='Chip identifier.'
    )
    group.add_argument(
        '-a', '--all',
        help='Generate labels for chips in package.',
        action="count"
    )
    group.add_argument(
        '-l', '--list',
        help='List all chips in package.',
        action="count"
    )
    parser.add_argument(
        '-i', '--input',
        metavar='dir',
        help=f'Input chip library file or directory (default: {DEFAULT_INPUT_DIR}). If a directory is specified all .yaml files in that directory will be loaded.',
        default=DEFAULT_INPUT_DIR
    )
    parser.add_argument(
        '-o', '--output',
        metavar='dir',
        help=f'Output directory (default: {DEFAULT_OUTPUT_DIR}).',
        default=DEFAULT_OUTPUT_DIR
    )
    parser.add_argument(
        '-f', '--font',
        metavar='file',
        help=f'TTF font to use (default: {DEFAULT_FONT}). Under Windows the system font directory is searched automatically.',
        default=DEFAULT_FONT
    )
    parser.add_argument(
        '--dpi',
        metavar='num',
        type=_dpi_range,
        help=f'Resolution in dots per inch (default: {DEFAULT_DPI}).',
        default=DEFAULT_DPI
    )
    parser.add_argument(
        '--invert',
        help='Invert label, for dead bug soldering.',
        action="count"
    )

    debug_group = parser.add_mutually_exclusive_group()

    debug_group.add_argument(
        '--debug',
        help="Print debugging statements.",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    debug_group.add_argument(
        '-v', '--verbose',
        help="Print additional information.",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    return parser.parse_args()

def main():
    args = parse_args()

    # Configure logging
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter())
    log.setLevel(args.loglevel)
    log.addHandler(handler)

    chip_list = ChipList()
    chip_list.load(args.input)
    if not chip_list.size:
        log.error('No chip loaded')
        return

    if args.list:
        for chip in sorted(chip_list.names, key=str.casefold):
            print(chip)
    elif args.all:
        for chip in chip_list:
            print('chip:', chip.scoped_id)
            print_chip_label(chip_list, chip.id, args)
    else:
        print_chip_label(chip_list, args.chip, args)

if __name__ == '__main__':
    import sys
    main()
