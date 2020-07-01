#!/usr/bin/env python3
# chip_list.py
#
from chip import Chip
import yaml
import logging
log = logging.getLogger(__name__)

def load_chip_list(filename) :
    chip_list = {}
    with open(filename, 'r') as ymlfile:
        yaml_chips = yaml.safe_load(ymlfile)
        for chipName, yaml_chip in yaml_chips.items():
            spacing = 6
            if 'type' in yaml_chip and yaml_chip['type'] == 'wide':
                spacing = 12
            chip = Chip(str(chipName), len(yaml_chip['pins']), rowSpacing = spacing)
            if 'name' in yaml_chip:
                chip.description = yaml_chip['name']

            chip.set_pins(yaml_chip['pins'])
            chip_list[str(chipName)] = chip
    return chip_list

def main():
    logging.basicConfig(level=logging.DEBUG)

    chip_list = load_chip_list('chips/chips.yaml')
    for name, chip in chip_list.items():
        chip.print_ASCII()
        print()

if __name__ == '__main__':
    main()
