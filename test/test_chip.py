#!/usr/bin/env python3
# test_chip.py

import pytest
from chiplabel import chip

def _createGood(id, pins=4) :
    a = chip.Chip(id, pins, library='')
    assert a.id == id
    return a

def _createBad(id, pins=4) :
    with pytest.raises(chip.ValidationError):
        chip.Chip(id, pins, library='')

def test_name():   
    GOOD_NAMES = ['goodName', 'goodName', 'good_name', 'good-name', 
        'other-good-name', '_good_name', 'good_name_', 'good-name-',
        '1', 'a1', '1a', '12345',
        'goodname12345678901234567890123456789012345678901234567890123456']
    for id in GOOD_NAMES:
        _createGood(id)

    BAD_NAMES = ['', 'bad name', '/badname', '\\badname', 'bad&name', 
        'bad!name', ' badname', 'badname ', '-badname',
        'badname1234567890123456789012345678901234567890123456789012345678']
    for id in BAD_NAMES:
        _createBad(id)

def test_pincount():
    GOOD_PINS = [4, 6, 10, 32, 64]
    for pins in GOOD_PINS:
        _createGood('id', pins)

    BAD_PINS = [0, 1, 2, 3, 5, 65]
    for pins in BAD_PINS:
        _createBad('id', pins)

def test_getsetitem():
    a = chip.Chip('Atmega328p', 8)

    assert a[1] == 'NC'
    assert a[8] == 'NC'
    a[1] = 'PIN1'
    a[8] = 'PIN8'
    assert a[1] == 'PIN1'
    assert a[8] == 'PIN8'

    with pytest.raises(IndexError):
        a[0] = "ERROR"
    with pytest.raises(IndexError):
        a[-1] = "ERROR"
    with pytest.raises(IndexError):
        a[29] = "ERROR"

def test_str():
    a = chip.Chip('chip', 4)
    assert a.__str__() == 'chip(4)'
    a = chip.Chip('chip', 4, 'lib')
    assert a.__str__() == 'lib/chip(4)'
    a = chip.Chip('chip', 4, 'lib/lab')
    assert a.__str__() == 'lib/lab/chip(4)'
    a = chip.Chip('chip', 4, r'lib\lab')
    assert a.__str__() == r'lib\lab/chip(4)'

def test_iter():
    a = chip.Chip('chip', 4)
    chip_iter = iter(a)
    assert chip_iter != None
    assert next(chip_iter) == 'NC'
    assert next(chip_iter) == 'NC'
    assert next(chip_iter) == 'NC'
    assert next(chip_iter) == 'NC'
    with pytest.raises(StopIteration):
        next(chip_iter)

def test_name():
    a = chip.Chip('chip', 4, 'lib')
    assert a.name == ''
    a.name = 'name'
    assert a.name == 'name'
    a.name = ' spacename '
    assert a.name == 'spacename'
    with pytest.raises(TypeError):
        a.name = 3
    with pytest.raises(TypeError):
        a.name = None
    with pytest.raises(TypeError):
        a.name = [1,2]

def test_description():
    a = chip.Chip('chip', 4, 'lib')
    assert a.description == ''
    a.description = 'name'
    assert a.description == 'name'
    a.description = ' space description '
    assert a.description == 'space description'

    with pytest.raises(TypeError):
        a.description = 3
    with pytest.raises(TypeError):
        a.description = None
    with pytest.raises(TypeError):
        a.description = [1,2]

def test_library():
    a = chip.Chip('chip', 4)
    assert a.library == ''
    assert a.id == 'chip'
    a.library = 'lib'
    assert a.library == 'lib'
    assert a.id == 'lib/chip'

    a.library = ' spacelib '
    assert a.library == 'spacelib'
    assert a.id == 'spacelib/chip'

    with pytest.raises(TypeError):
        a.library = 3
    with pytest.raises(TypeError):
        a.library = None
    with pytest.raises(TypeError):
        a.library = [1,2]

    b = chip.Chip('chip', 4, ' spacelib ')
    assert a.library == 'spacelib'

def test_display_name():
    a = chip.Chip('chip', 4, 'lib')
    assert a.display_name == 'chip'
    assert a.name == ''
    a.name = 'myname'
    assert a.display_name == 'myname'
    a.name = ''
    assert a.display_name == 'chip'

def test_full_name():
    a = chip.Chip('chip', 4, 'lib')
    assert a.description == ''
    assert a.full_name == 'chip'
    a.description = 'desc'
    assert a.full_name == 'chip desc'
    a.description = '  '
    assert a.full_name == 'chip'

def test_id():
    a = chip.Chip('chip', 4, 'lib')    
    assert a.id == 'lib/chip'
    a.library = ''
    assert a.id == 'chip'

def test_scoped_id():
    a = chip.Chip('chip', 4, 'lib')    
    assert a.scoped_id == 'lib/chip'
    a.library = ''
    assert a.scoped_id == 'chip'

def test_unscoped_id():
    a = chip.Chip('chip', 4, 'lib')    
    assert a.unscoped_id == 'chip'
    a.library = ''
    assert a.unscoped_id == 'chip'

def test_alias():
    a = chip.Chip('chip', 4, 'lib', config_flag='flag')
    a.name = 'aname'
    a.description = 'adescription'
    a.set_pins(['1','2','3','4'])

    alias = a.create_alias('alias')
    assert alias.id == 'lib/alias'
    assert alias.name == 'aname'
    assert alias.description == 'adescription'
    assert alias[1] == '1'
    assert alias[4] == '4'

    alias.name = 'newname'
    assert alias.name == 'newname'
    assert a.name == 'aname'

    alias.description = 'newdesc'
    assert alias.description == 'newdesc'
    assert a.description == 'adescription'

    # This is a shallow copy so pins and config are shared
    a[1] = 'newpin1'
    assert a[1] == 'newpin1'
    assert alias[1] == 'newpin1'

    assert a.config['config_flag'] == 'flag'
    assert alias.config['config_flag'] == 'flag'
    alias.config['config_flag'] = 'newflag'
    assert a.config['config_flag'] == 'newflag'

def test_set_pins():
    a = chip.Chip('chip', 4)
    assert len(a) == 4
    a.set_pins(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    assert len(a) == 8
    a.set_pins(['1', '2', '3', '4'])
    assert len(a) == 4

    with pytest.raises(ValueError):
        a.set_pins(None)
    with pytest.raises(ValueError):
        a.set_pins(124)
    with pytest.raises(ValueError):
        a.set_pins(12.34)
    with pytest.raises(ValueError):
        a.set_pins('abc')
    with pytest.raises(ValueError):
        a.set_pins({'a':True})
    with pytest.raises(chip.ValidationError):
        a.set_pins([])
    with pytest.raises(chip.ValidationError):
        a.set_pins(['1','2','3'])

def test_len():
    a = chip.Chip('chip', 28)
    assert len(a) == 28

    b = chip.Chip('chip', 14)
    assert len(b) == 14

