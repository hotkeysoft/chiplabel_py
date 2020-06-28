#!/usr/bin/env python3
from PIL import ImageFont, ImageDraw, Image
from chip import Chip
from chip_printer import ChipPrinter
import math

def main(args):
    chip = Chip('7404', 14)
    pins = ['1A', '1Y', '2A', '2Y', '3A', '3Y', 'GND', '4Y', '4A', '5Y', '5A', '6Y', '6A', 'VCC']
    for pinnum, pin in enumerate(chip, 1):
        chip[pinnum] = pins[pinnum-1]

    printer = ChipPrinter()
    image = printer.print_chip(chip)
    image.save("./out.png", dpi=(printer.config['dpi'], printer.config['dpi']))

    # if len(args) < 3:
    #     raise SystemExit(f'Usage: %s' % args[0])

if __name__ == '__main__':
    import sys
    main(sys.argv)
