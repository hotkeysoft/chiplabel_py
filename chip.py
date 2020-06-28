#!/usr/bin/env python3
# chip.py
#
from typedproperty import String

class Chip:
    name = String('name')
    description = String('description')
    _pins = {}

    config = {
        "pinSpacing": 2.54,
        "rowSpacing": 6, # in mm, 6 for narrow, 12 for wide
    }

    def __init__(self, name, pinCount, description='', **kwargs):

        if pinCount < 4 or pinCount > 64:
            raise ValueError(f'Pin count must be [4,64]')
        if pinCount % 2:
            raise ValueError('Pin count must be even')

        self.name = name
        self._pins = ["NC"] * pinCount
        self.description = description

        if kwargs:
            self.config = {**self.config, **kwargs}

    def __str__(self):
        return f'{self.name}({len(self._pins)})'

    def __repr__(self):
        return f'chip.Chip({self.name}({len(self._pins)}))'

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
    def size(self):
         return len(self._pins)

    def printASCII(self):
        pinCount = len(self._pins)
        maxLen = max(len(pin) for pin in self._pins)
        fullWidth = maxLen*2 + 11
        print(f'{self.name:^{fullWidth}}')
        print('  ','-'*(2*maxLen + 5))
        for row in range(pinCount//2):
            rightSizePin = pinCount - row - 1
            print(f'{row+1:2} | {self._pins[row]:{maxLen}} {self._pins[rightSizePin]:>{maxLen}} | {rightSizePin+1}')
        print('  ','-'*(2*maxLen + 5))

def main():
    a = Chip('Atmega328p', 28)
    b = Chip('7404', 14)

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

    bPins = ['1A', '1Y', '2A', '2Y', '3A', '3Y', 'GND', '4Y', '4A', '5Y', '5A', '6Y', '6A', 'VCC']
    for pinnum, pin in enumerate(b, 1):
        b[pinnum] = bPins[pinnum-1]


    for pinnum, pin in enumerate(a, 1):
        print(f'{pinnum}: {pin}')

    a.printASCII()
    b.printASCII()

    d = Chip('testargs', 28, rowSpacing=12)
    print(d.config)

if __name__ == '__main__':
    main()
