#!/usr/bin/env python3
# test_chip_list.py

import pkg_resources
import pytest
from chiplabel import chip
from chiplabel.chip_list import ChipList

TEST_DATA_DIR = pkg_resources.resource_filename('test', 'data')

def test_load_file(caplog):
    chip_list = ChipList()
    
    with pytest.raises(IOError):
        chip_list.load('')
    with pytest.raises(IOError):
        chip_list.load('bad')

    chip_list.load(f'{TEST_DATA_DIR}/chip0.yaml')
    assert "No chip data" in caplog.text    
    caplog.clear()
    assert len(chip_list) == 0

    chip_list.load(f'{TEST_DATA_DIR}/chip1.yaml')
    assert caplog.text == ''
    assert len(chip_list) == 1

    chip_list.load(f'{TEST_DATA_DIR}/chip2.yaml')
    assert "Duplicate" in caplog.text    
    assert len(chip_list) == 3

def test_load_directory():
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}')
    assert len(chip_list) == 3

def test_ids():
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}')

    assert chip_list.names == ['chip1/555', 'chip2/555', 'chip2/TestChip']
    assert chip_list.global_names == ['555', 'TestChip']

def test_iter():
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}')

    chipNames = [chip.unscoped_id for chip in chip_list]
    assert chipNames == ['555', '555', 'TestChip']

def test_find_chip():
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}')

    with pytest.raises(ValueError):
        chip_list.find_chip(None)

    with pytest.raises(ValueError):
        chip_list.find_chip(555)

    chip = chip_list.find_chip('555')
    assert chip != None
    assert chip.id in ['chip1/555', 'chip2/555']

    chip = chip_list.find_chip('chip1/555')
    assert chip != None
    assert chip.id == 'chip1/555'

    chip = chip_list.find_chip('/555')
    assert chip == None

    chip = chip_list.find_chip('bad/555')
    assert chip == None

    chip = chip_list.find_chip('chip1/')
    assert chip == None

    chip = chip_list.find_chip('chip1/bad')
    assert chip == None

def test_chip_attributes():
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}')

    chip = chip_list['TestChip']
    assert chip
    assert chip.name == 'myName'
    assert chip.description == 'myDescription'
    assert chip.config['rowSpacing'] == 12
    assert [pin for pin in chip] == ['P1', 'P2', 'P3', 'P4']
    
def test_family_7400(caplog):
    def good_lookup(chip_id):
        chip = chip_list[chip_id]
        assert chip
        assert chip.id == f'7400a/{chip_id}'

    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}/family/7400a.yaml')
    assert len(chip_list) == 1
    assert len(chip_list.global_names) > 10

    ALIASES = ['74999', '74LS999', '74F999', '74HCT999']
    for alias in ALIASES:
        good_lookup(alias)

    # For now aliases exist only in the global (unscoped) list
    assert chip_list['7400a/74LS999'] == None

    # Chip with family=7400 but prefix is not 74
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}/family/7400b.yaml')
    assert len(chip_list) == 1
    assert len(chip_list.global_names) == 1
    assert "ERROR" in caplog.text    
    assert "missing 74 prefix" in caplog.text

def test_bad_yaml(caplog):
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}/bad/bad_yaml.yaml')
    assert len(chip_list) == 0
    assert 'ERROR' in caplog.text

def test_empty():
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}/chip0.yaml')
    assert len(chip_list) == 0

def test_bad_chip(caplog):
    # Chip with validation error
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}/bad/bad_chip.yaml')
    assert 'Error adding chip [bad_chip/Test!Chip]' in caplog.text
    assert 'Error adding chip [bad_chip/5pins]' in caplog.text
    assert 'Error adding chip [bad_chip/nopins]' in caplog.text    
    assert len(chip_list) == 1

def test_bad_type(caplog):
    # will load chip with bad type, with warning
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}/bad/bad_type.yaml')
    assert len(chip_list) == 2
    chip = chip_list['TestChip']
    assert chip
    assert chip.name == 'myName'
    assert chip.description == 'myDescription'
    assert chip.config['rowSpacing'] == 6
    assert 'WARNING' in caplog.text
    assert 'Unknown type attribute' in caplog.text

def test_bad_family(caplog):
    # will load chip with bad family, with warning
    # no alias will be loaded
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}/bad/bad_family.yaml')
    assert len(chip_list) == 2    
    assert len(chip_list.global_names) == 2    
    chip = chip_list['TestChip']
    assert chip.name == 'myName'
    assert chip.description == 'myDescription'
    assert chip.config['rowSpacing'] == 6 
    assert 'WARNING' in caplog.text
    assert 'Unknown family' in caplog.text

def test_hidden_chips():
    # chip ids that start with _ are skipped
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}/bad/skip.yaml')
    assert len(chip_list) == 2    
    assert len(chip_list.global_names) == 2

def test_bad_dup(caplog):
    # chip list with duplicate definition
    # duplicates are silently skipped due to yaml library implementation
    chip_list = ChipList()
    chip_list.load(f'{TEST_DATA_DIR}/bad/dup.yaml')
    assert len(chip_list) == 2    
    assert len(chip_list.global_names) == 2    
    chip = chip_list['555']
    assert chip.name == 'dup'
