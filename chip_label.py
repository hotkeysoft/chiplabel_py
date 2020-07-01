#!/usr/bin/env python3
from args import parse_args
from chip import Chip
from chip_list import ChipList
from chip_printer import ChipPrinter
import logging
log = logging.getLogger()

def _to_chip_list(chip_list, chip_ids):
    chips = []
    for chip_id in chip_ids:
        chip = chip_list[chip_id]
    if not chip:
        log.error('Chip not found: %s', chip_id)
        return
    chips.append(chip)
    return chips

def print_chip(chip_list, args):
    if not args.page:
        for chip in chip_list:
            if args.text:
                print()
                chip.print_ASCII()
            else:
                log.info('Generating label for chip: %s', chip.id)
                print_chip_image(chip, args)
    else:
        raise NotImplementedError()

def print_chip_image(chip, args):

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
    if not chip_list.size:
        log.error('No chip loaded')
        return

    if args.list:
        for chip in sorted(chip_list.names, key=str.casefold):
            print(chip)
    elif args.all:
        print_chip(chip_list, args)
    else:
        chips = [chip_list.find_chip(chip) for chip in args.chip]
        print_chip(chips, args)

if __name__ == '__main__':
    import sys
    MIN_PYTHON = (3, 6)
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)
    main()
