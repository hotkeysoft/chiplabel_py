#!/usr/bin/env python3
from PIL import ImageFont, ImageDraw, Image
from chip import Chip
from chip_printer import ChipPrinter
from chip_list import load_chip_list
import math
import argparse

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

    printer = ChipPrinter(**config)
    chip = chip_list[chip_name]
    image = printer.print_chip(chip)
    output_file = f"{output_dir}{chip_name}.png"
    image.save(output_file, dpi=(printer.config['dpi'], printer.config['dpi']))
    print(f'Output saved to {output_file}')

def _dpi_range(string):
    try:
        value = int(string)
        if value < MIN_DPI or value > MAX_DPI:
            raise argparse.ArgumentTypeError(f'{value} is not in range [{MIN_DPI}, {MAX_DPI}]')
    except ValueError:
        raise argparse.ArgumentTypeError(f'{string} is not an integer value')
    return value

def main():
    parser = argparse.ArgumentParser(description='Generate footprint images for chips')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--chip', metavar='name', help='chip identifier')
    group.add_argument('-a', '--all', help='generate labels for chips in package', action="count")
    group.add_argument('-l', '--list', help='list all chips in package', action="count")
    parser.add_argument('-o', '--output', metavar='dir', help='output directory (default: ./out)', default='./out')
    parser.add_argument('-f', '--font', metavar='file', help='ttf font to use (default: ./fonts/CascadiaMono.ttf). Under Windows the system font directory is searched automatically.', default='./fonts/CascadiaMono.ttf')
    parser.add_argument('-d', '--dpi', metavar='num', type=_dpi_range, help='resolution in dots per inch (default: 300)', default=300)
    #parser.add_argument('-v', '--verbose', help='outputs additional information', action='count')
    args = parser.parse_args()

    chip_file = 'chips/chips.yaml'
    chip_list = load_chip_list(chip_file)
    print(f'loaded {len(chip_list)} chips from {chip_file}')

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
