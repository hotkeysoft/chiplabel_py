#!/usr/bin/env python3
# chip.py
#
import copy
import re
import logging
from .typed_property import StrippedString, RegexString
log = logging.getLogger(__name__)

# Allow letters, numbers, underscore and dash (except as first character)
VALID_ID_REGEX = re.compile(r'^\w[-\w]{0,63}$')
# Same rules + also allows empty string
VALID_LIBRARY_REGEX  = re.compile(r'^(?:\w[-\w]{0,63})?$')

class Chip:
    _id = None
    _pins = {}

    name = StrippedString('name')
    #library = StrippedString('library')#, VALID_NAME)
    library = RegexString('library', VALID_LIBRARY_REGEX)
    description = StrippedString('description')

    config = {
        "pinSpacing": 2.54,
        "rowSpacing": 6, # in mm, 6 for narrow, 12 for wide
    }

    def __init__(self, id, pinCount, library='', **kwargs):
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
        return f'chip.Chip({self.id}, {len(self._pins)})'

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
        if not isinstance(value, (float, int, str)):
            raise ValueError(f'Invalid pin value for pin: {index}')
        self._pins[index-1] = str(value)

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
        if any([not isinstance(pin, (float, int, str)) for pin in pins]):
            raise ValueError('Invalid pin(s) in pin list')
        log.debug('Chip[%s].set_pins(%s)', self.id, pins)
        self._pins = [str(pin) for pin in pins]

    @staticmethod
    def _validate_pin_count(pinCount):
        if pinCount < 4 or pinCount > 64:
            raise ValidationError(f'Pin count must be [4,64]')
        if pinCount % 2:
            raise ValidationError('Pin count must be even')

    @staticmethod
    def _validate_chip_id(id):
        if not VALID_ID_REGEX.match(id):
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
