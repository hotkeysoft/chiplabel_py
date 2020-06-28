#!/usr/bin/env python3
# chip_list.py
#
from chip import Chip
import yaml # PyYAML

def load_chip_list(filename) :
    chip_list = []
    with open(filename, 'r') as ymlfile:
        yaml_chips = yaml.safe_load(ymlfile)
        for chipName in yaml_chips:
            yaml_chip = yaml_chips[chipName]
            chip = Chip(str(chipName), len(yaml_chip['pins']))
            if 'name' in yaml_chip:
                chip.description = yaml_chip['name']
            chip.set_pins(yaml_chip['pins'])
            chip_list.append(chip)
    return chip_list

def main():
    chip_list = load_chip_list('chips/chips.yaml')
    for chip in chip_list:
        chip.print_ASCII()
        print()

if __name__ == '__main__':
    main()
