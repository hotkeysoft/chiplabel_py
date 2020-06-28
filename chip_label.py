#!/usr/bin/env python3
from PIL import ImageFont, ImageDraw, Image
from chip import Chip
from chip_printer import ChipPrinter
from chip_list import load_chip_list
import math
import argparse

def print_chip_label(chip_list, chip_name):
    if chip_name not in chip_list:
        raise SystemExit(f'Chip not found: {chip_name}')

    chip = chip_list[chip_name]
    printer = ChipPrinter()
    image = printer.print_chip(chip)
    output_file = f"out/{chip_name}.png"
    image.save(output_file, dpi=(printer.config['dpi'], printer.config['dpi']))
    print(f'Output saved to {output_file}')

def main():
    parser = argparse.ArgumentParser(description='Generate footprint images for chips')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--chip', help='chip identifier')
    group.add_argument('-a', '--all', help='generate labels for chips in package', action="count")
    group.add_argument('-l', '--list', help='list all chips in package', action="count")
    args = parser.parse_args()

    chip_file = 'chips/chips.yaml'
    chip_list = load_chip_list(chip_file)
    print(f'loaded {len(chip_list)} chips from {chip_file}')

    if args.list:
        for chip in sorted(chip_list, key=str.casefold):
            print(chip)
    elif args.all:
        for chip in chip_list:
            print_chip_label(chip_list, chip)    
    else:
        print_chip_label(chip_list, args.chip)

if __name__ == '__main__':
    import sys
    main()
