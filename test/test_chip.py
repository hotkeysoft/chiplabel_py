#!/usr/bin/env python3
# test_chip.py

import pytest
from chiplabel import chip

def _create_good(id, pins=4) :
    a = chip.Chip(id, pins, library='')
    assert a.id == id
    return a

def _create_bad(id, pins=4) :
    with pytest.raises(chip.ValidationError):
        chip.Chip(id, pins, library='')  

def test_name():   
    GOOD_NAMES = ['goodName', 'goodName', 'good_name', 'good-name', 
        'other-good-name', '_good_name', 'good_name_', 'good-name-',
        '1', 'a1', '1a', '12345',
        'goodname12345678901234567890123456789012345678901234567890123456']
    for id in GOOD_NAMES:
        _create_good(id)

    BAD_NAMES = ['', 'bad name', '/badname', '\\badname', 'bad&name', 
        'bad!name', ' badname', 'badname ', '-badname',
        'badname1234567890123456789012345678901234567890123456789012345678']
    for id in BAD_NAMES:
        _create_bad(id)

def test_pincount():
    GOOD_PINS = [4, 6, 10, 32, 64]
    for pins in GOOD_PINS:
        _create_good('id', pins)

    BAD_PINS = [0, 1, 2, 3, 5, 65]
    for pins in BAD_PINS:
        _create_bad('id', pins)

def test_getsetitem():
    a = chip.Chip('Chip', 8)

    assert a[1] == 'NC'
    assert a[8] == 'NC'
    a[1] = 'PIN1'
    a[8] = 'PIN8'
    assert a[1] == 'PIN1'
    assert a[8] == 'PIN8'

def test_bad_setitem():
    a = chip.Chip('Chip', 8)

    with pytest.raises(IndexError):
        a[0] = "ERROR"
    with pytest.raises(IndexError):
        a[-1] = "ERROR"
    with pytest.raises(ValueError):
        a[1] = [1,2,3]
    with pytest.raises(ValueError):
        a[1] = {'a':123}
    with pytest.raises(ValueError):
        a[1] = None

    with pytest.raises(IndexError):
        pin = a[0]
    with pytest.raises(IndexError):
        pin = a[-1]
    with pytest.raises(IndexError):
        pin = a[29]

def test_str():
    a = chip.Chip('chip', 4)
    assert a.__str__() == 'chip(4)'
    a = chip.Chip('chip', 4, 'lib')
    assert a.__str__() == 'lib/chip(4)'

def test_repr():
    a = chip.Chip('chip', 4)
    assert a.__repr__() == 'chip.Chip(chip, 4)'
    a = chip.Chip('chip', 4, 'lib')
    assert a.__repr__() == 'chip.Chip(lib/chip, 4)'

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
    def good_library_name(name):
        a.library = name
        assert a.library == name.strip()
        assert a.id == f'{name.strip()}/chip'

    def bad_library_name(name):
        with pytest.raises(TypeError):
            a.library = name
        with pytest.raises(TypeError):
            chip.Chip('chip', 4, name)

    a = chip.Chip('chip', 4)
    assert a.library == ''
    assert a.id == 'chip'

    GOOD_NAMES = ['lib', ' spacelib ', 'space-lib', 'space_lib']
    for name in GOOD_NAMES:
        good_library_name(name)

    with pytest.raises(TypeError):
        a.library = 3
    with pytest.raises(TypeError):
        a.library = None
    with pytest.raises(TypeError):
        a.library = [1,2]

    BAD_NAMES = ['-spaceLib', '-a', 'a/b', r'a\b']
    for name in BAD_NAMES:
        bad_library_name(name)

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

def test_good_set_pins():
    a = chip.Chip('chip', 4)
    assert len(a) == 4

    a.set_pins(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    assert len(a) == 8
    assert a[1] == 'a'
    assert a[8] == 'h'

    a.set_pins(['1', '2', '3', '4'])
    assert len(a) == 4
    assert a[1] == '1'
    assert a[4] == '4'

    a.set_pins(['1', 2, '3', 4])
    assert len(a) == 4
    assert a[1] == '1'
    assert a[4] == '4'

def test_bad_set_pins():
    a = chip.Chip('chip', 4)
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
    with pytest.raises(chip.ValidationError):
        a.set_pins(['1',None,'3'])
    with pytest.raises(chip.ValidationError):
        a.set_pins(['1',[1,2],'3'])
    with pytest.raises(chip.ValidationError):
        a.set_pins(['1',{},'3'])
    with pytest.raises(chip.ValidationError):
        a.set_pins(['1',{'a':True},'3'])

def test_len_size():
    a = chip.Chip('chip', 28)
    assert len(a) == 28
    assert a.size == 28

    b = chip.Chip('chip', 14)
    assert len(b) == 14
    assert b.size == 14

def test_kwargs():
    a = chip.Chip('chip', 28)
    assert a.config['rowSpacing'] == 6
    assert a.config['pinSpacing'] == 2.54

    a = chip.Chip('chip', 28, pinSpacing=1.23, dpi=300, rowSpacing=12)
    assert a.config['dpi'] == 300
    assert a.config['rowSpacing'] == 12
    assert a.config['pinSpacing'] == 1.23

def test_print_ASCII(capsys):
    a = chip.Chip('chip', 4)
    a.description = 'desc'
    a.set_pins(['P1', 'P2', 3, 'P4'])
    a.print_ASCII()

    captured = capsys.readouterr()
    assert 'chip' in captured.out
    assert 'desc' in captured.out
    assert '1 | P1' in captured.out
    assert '2 | P2' in captured.out
    assert '3 | 3' in captured.out
    assert 'P4 | 4' in captured.out
  
