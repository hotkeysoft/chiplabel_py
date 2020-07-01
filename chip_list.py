#!/usr/bin/env python3
# chip_list.py
#
import os
from chip import Chip
import yaml
import logging
log = logging.getLogger(__name__)

def load_chip_list(path):
    log.debug('load_chip_list(%s)', path)
    if os.path.isfile(path):
        return load_chip_list_file(path)
    elif os.path.isdir(path):
        chip_list = {}
        for file in os.listdir(path):
            if file.endswith(".yaml"):
                fullpath = os.path.normpath(os.path.join(path, file))
                chip_list.update(load_chip_list_file(fullpath))
        return chip_list
    else:
        raise IOError('input must be a file or directory')

def load_chip_list_file(filename):
    log.debug('load_chip_list_file(%s)', filename)
    chip_list = {}
    with open(filename, 'r') as ymlfile:
        yaml_chips = yaml.safe_load(ymlfile)
        for id, yaml_chip in yaml_chips.items():
            spacing = 6
            if 'type' in yaml_chip and yaml_chip['type'] == 'wide':
                spacing = 12
            chip = Chip(str(id), len(yaml_chip['pins']), rowSpacing = spacing)
            if 'name' in yaml_chip:
                chip.name = yaml_chip['name']
            if 'description' in yaml_chip:
                chip.description = yaml_chip['description']

            chip.set_pins(yaml_chip['pins'])
            chip_list[str(id)] = chip
    log.info(f'Loaded %d chips from %s', len(chip_list), filename)
    return chip_list

def main():
    logging.basicConfig(level=logging.DEBUG)

    chip_list = load_chip_list('chips/chips.yaml')
    for name, chip in chip_list.items():
        chip.print_ASCII()
        print()

if __name__ == '__main__':
    main()
