#!/usr/bin/env python3
from PIL import ImageFont, ImageDraw, Image
from chip import Chip
from chip_printer import ChipPrinter
from chip_list import load_chip_list
import math
import argparse
import logging
log = logging.getLogger(__name__)

MIN_DPI = 50
MAX_DPI = 2000

def print_chip_label(chip_list, chip_name, args):
    if chip_name not in chip_list:
        raise SystemExit(f'Chip not found: {chip_name}')

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
    chip = chip_list[chip_name]
    image = printer.print_chip(chip)
    output_file = f"{output_dir}{chip_name}.png"
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

def main():
    chip_file = 'chips/chips.yaml'

    parser = argparse.ArgumentParser(
        description='Generate footprint images for chips.',
        epilog=f'Chip definitions are loaded from {chip_file}')
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
        '-o', '--output',
        metavar='dir',
        help='Output directory (default: ./out).',
        default='./out'
    )
    parser.add_argument(
        '-f', '--font',
        metavar='file',
        help='TTF font to use (default: ./fonts/CascadiaMono.ttf). Under Windows the system font directory is searched automatically.',
        default='./fonts/CascadiaMono.ttf'
    )
    parser.add_argument(
        '-d', '--dpi',
        metavar='num',
        type=_dpi_range,
        help='Resolution in dots per inch (default: 300).',
        default=300
    )
    parser.add_argument(
        '-i', '--invert',
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
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    chip_list = load_chip_list(chip_file)
    log.info(f'loaded {len(chip_list)} chips from {chip_file}')

    if args.list:
        for chip in sorted(chip_list, key=str.casefold):
            print(chip)
    elif args.all:
        for chip in chip_list:
            print_chip_label(chip_list, chip, args)
    else:
        print_chip_label(chip_list, args.chip, args)

if __name__ == '__main__':
    import sys
    main()
