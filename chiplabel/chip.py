#!/usr/bin/env python3
# chip.py
#
import copy
import re
import logging
from .typed_property import String
log = logging.getLogger(__name__)

VALID_CHIP_ID = re.compile('^[-\w]+$')

class Chip:
    _id = None
    _pins = {}

    name = String('name')
    library = String('library')
    description = String('description')

    config = {
        "pinSpacing": 2.54,
        "rowSpacing": 6, # in mm, 6 for narrow, 12 for wide
    }

    def __init__(self, id, pinCount, library, **kwargs):
        log.debug('Chip.__init__("%s", %d, library="%s")',
            id, pinCount, library)

        self._validate_chip_id(id)
        self._validate_pin_count(pinCount)

        self._id = id
        self.name = ''
        self.description = ''
        self.library = library

        self._pins = ["NC"] * pinCount

        if kwargs:
            self.config = {**self.config, **kwargs}

    def __str__(self):
        return f'{self.id}({len(self._pins)})'

    def __repr__(self):
        return f'chip.Chip({self.id}({len(self._pins)}))'

    def __len__(self):
        return len(self._pins)

    def __iter__(self):
        return self._pins.__iter__()

    def __getitem__(self, index):
        if index < 1 or index > len(self._pins):
            raise IndexError(f'Pin number out of range: {index}')
        return self._pins[index-1]

    def __setitem__(self, index, value):
        if index < 1 or index > len(self._pins):
            raise IndexError(f'Pin number out of range: {index}')
        self._pins[index-1] = value

    @property
    def display_name(self):
        if len(self.name):
            return self.name
        else:
            return self.unscoped_id

    @property
    def full_name(self):
        return f'{self.display_name} {self.description}'.rstrip()

    @property
    def id(self):
        return self.scoped_id

    @property
    def unscoped_id(self):
        return self._id

    @property
    def scoped_id(self):
        return f'{self.library}/{self._id}' if len(self.library) else self._id

    def create_alias(self, id):
        # aliases are shallow copies
        alias = copy.copy(self)
        alias._id = id
        return alias        

    def set_pins(self, pins):
        if not isinstance(pins, list):
            raise ValueError('Expected pin list')
        self._validate_pin_count(len(pins))
        log.debug('Chip[%s].set_pins(%s)', self.id, pins)
        self._pins = pins.copy()

    @staticmethod
    def _validate_pin_count(pinCount):
        if pinCount < 4 or pinCount > 64:
            raise ValidationError(f'Pin count must be [4,64]')
        if pinCount % 2:
            raise ValidationError('Pin count must be even')

    @staticmethod
    def _validate_chip_id(id):
        if not VALID_CHIP_ID.match(id):
            raise ValidationError(f'Invalid characters in chip id')

    @property
    def size(self):
         return len(self._pins)

    def print_ASCII(self):
        pinCount = len(self._pins)
        maxLen = max(len(pin) for pin in self._pins)
        fullWidth = maxLen*2 + 11
        print(f'{self.full_name:^{fullWidth}}')
        print('  ','-'*(2*maxLen + 5))
        for row in range(pinCount//2):
            rightSizePin = pinCount - row - 1
            print(f'{row+1:2} | {self._pins[row]:{maxLen}} {self._pins[rightSizePin]:>{maxLen}} | {rightSizePin+1}')
        print('  ','-'*(2*maxLen + 5))

class Error(Exception):
    """Base class for exceptions in this module."""
    pass
class ValidationError(Error):
    """Raised when an invalid condition is found."""
    pass

def main():
    logging.basicConfig(level=logging.DEBUG)

    a = Chip('Atmega328p', 28)
    b = Chip('7404', 14, description='NOT', library='TTL')

    print ("A len: ", len(a))
    print ("B len: ", len(b))

    print(a)
    print(b)

    a[1] = "PIN1"
    a[28] = "PIN28"

    #test errors
    #a[0] = "ERROR"
    #a[29] = "ERROR"
    #c = Chip('0pins', 0)
    #d = Chip('3pins', 3)
    #e = Chip('66pins', 66)
    #f = Chip('evenpins', 15)
    #g = Chip('/badid1', 8)
    #h = Chip('bad id2', 8)
    #i = Chip('', 8)

    bPins = ['1A', '1Y', '2A', '2Y', '3A', '3Y', 'GND', '4Y', '4A', '5Y', '5A', '6Y', '6A', 'VCC']
    for pinnum, pin in enumerate(b, 1):
        b[pinnum] = bPins[pinnum-1]


    for pinnum, pin in enumerate(a, 1):
        print(f'{pinnum}: {pin}')

    a.print_ASCII()
    print()
    b.print_ASCII()
    print()

    d = Chip('testargs', 28, rowSpacing=12)
    print(d.config)

if __name__ == '__main__':
    main()
