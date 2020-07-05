#!/usr/bin/env python3
# test_chip_printer.py

import pkg_resources
import pytest
from PIL import Image
from PIL import ImageChops
from chiplabel import chip
from chiplabel.chip_list import ChipList
from chiplabel.chip_printer import ChipPrinter

CREATE_REFERENCES = False
FONT_DIR = pkg_resources.resource_filename('chiplabel', 'fonts')
DEFAULT_FONT = f'{FONT_DIR}/CascadiaMono.ttf'
REF_DIR = pkg_resources.resource_filename('test', 'data/img')

def test_init():
    c = ChipPrinter()
    assert c.config['dpi'] == 300
    assert c.config['invert'] == False
    assert c.config['font'] == ''
    assert c.font

    c = ChipPrinter(invert=True, foo='bar', dpi=600)
    assert c.config['invert'] == True
    assert c.config['dpi'] == 600
    assert c.config['foo'] == 'bar'
    assert c.font

def test_font(caplog):
    c = ChipPrinter() # No font, warning
    assert 'WARNING' in caplog.text
    assert 'Unable to load font' in caplog.text
    assert c.font
    caplog.clear()


    c = ChipPrinter(font='bad_font')
    assert 'WARNING' in caplog.text
    assert 'Unable to load font' in caplog.text
    assert 'bad_font' in caplog.text
    assert c.font    
    caplog.clear()

    c = ChipPrinter(font=DEFAULT_FONT)
    assert caplog.text == ''
    assert c.font
    print(c.font)
    assert c.font.getname() == ('Cascadia Mono', 'Regular')
    caplog.clear()

def test_get_chip_size():
    narrow_chip = chip.Chip('narrow', 8, rowSpacing=6)
    wide_chip = chip.Chip('wide', 8, rowSpacing=12)
    weird_chip = chip.Chip('weird', 8, pinSpacing=5.08, rowSpacing=12)

    p = ChipPrinter(dpi=100)      
    assert p.get_chip_size(narrow_chip) == (24, 40)
    assert p.get_chip_size(wide_chip) == (48, 40)
    assert p.get_chip_size(weird_chip) == (48, 80)

    p = ChipPrinter(dpi=200)      
    assert p.get_chip_size(narrow_chip) == (48, 80)
    assert p.get_chip_size(wide_chip) == (95, 80)
    assert p.get_chip_size(weird_chip) == (95, 160)

    p = ChipPrinter(dpi=1000)      
    assert p.get_chip_size(narrow_chip) == (237, 400)
    assert p.get_chip_size(wide_chip) == (473, 400)
    assert p.get_chip_size(weird_chip) == (473, 800)

def _create_reference(chip_printer, chip, name):
    chip_printer.print_chip_to_file(chip, f'{REF_DIR}/{name}.png')

def _compare_reference(chip_printer, chip, name):
    ref = Image.open(f'{REF_DIR}/{name}.png')
    assert ref

    test_image = chip_printer.print_chip(chip)
    assert test_image
    assert test_image.size == ref.size
   
    diff = ImageChops.difference(test_image, ref)

    if diff.getbbox():
        diffname = f'diff_{name}.png'
        diff.save(diffname)
        pytest.fail(f"image different from ref, difference saved to {diffname}")

def test_print_chip():
    pins = [f'A{n}' for n in range(1, 9)]
    pins[3] = '/A4'
    pins[7] = '/A8'
    normal_chip = chip.Chip('normal', 8)
    normal_chip.description = 'desc'
    normal_chip.set_pins(pins)
    wide_chip = chip.Chip('wide', 8, rowSpacing=12)
    wide_chip.description = 'desc'
    wide_chip.set_pins(pins)

    if CREATE_REFERENCES:
        _create_reference(ChipPrinter(font=DEFAULT_FONT, dpi=300), normal_chip, 'nn300')
        _create_reference(ChipPrinter(font=DEFAULT_FONT, dpi=300), wide_chip, 'nw300')
        _create_reference(ChipPrinter(font=DEFAULT_FONT, dpi=300, invert=True), normal_chip, 'in300')
        _create_reference(ChipPrinter(font=DEFAULT_FONT, dpi=300, invert=True), wide_chip, 'iw300')
        _create_reference(ChipPrinter(font=DEFAULT_FONT, dpi=600), normal_chip, 'nn600')
        _create_reference(ChipPrinter(font=DEFAULT_FONT, dpi=600), wide_chip, 'nw600')
        _create_reference(ChipPrinter(font=DEFAULT_FONT, dpi=600, invert=True), normal_chip, 'in600')
        _create_reference(ChipPrinter(font=DEFAULT_FONT, dpi=600, invert=True), wide_chip, 'iw600')

    _compare_reference(ChipPrinter(font=DEFAULT_FONT, dpi=300), normal_chip, 'nn300')
    _compare_reference(ChipPrinter(font=DEFAULT_FONT, dpi=300), wide_chip, 'nw300')
    _compare_reference(ChipPrinter(font=DEFAULT_FONT, dpi=300, invert=True), normal_chip, 'in300')
    _compare_reference(ChipPrinter(font=DEFAULT_FONT, dpi=300, invert=True), wide_chip, 'iw300')
    _compare_reference(ChipPrinter(font=DEFAULT_FONT, dpi=600), normal_chip, 'nn600')
    _compare_reference(ChipPrinter(font=DEFAULT_FONT, dpi=600), wide_chip, 'nw600')
    _compare_reference(ChipPrinter(font=DEFAULT_FONT, dpi=600, invert=True), normal_chip, 'in600')
    _compare_reference(ChipPrinter(font=DEFAULT_FONT, dpi=600, invert=True), wide_chip, 'iw600')

def _save_to_file(tmpdir, chip_printer, chip, dpi, ext):
    out_file = f'{tmpdir}/test_{dpi}.{ext}'

    chip_printer.print_chip_to_file(chip, out_file)

    image = Image.open(out_file)
    assert image
    assert image.info['dpi'] == (dpi, dpi)

def test_print_chip_to_file(tmpdir):
    c = chip.Chip('normal', 8)

    p = ChipPrinter()
    with pytest.raises(AttributeError):
        p.print_chip_to_file(None, 'out.png')
    with pytest.raises(ValueError):
        p.print_chip_to_file(c, None)
    with pytest.raises(ValueError):        
        p.print_chip_to_file(c, '')

    p = ChipPrinter(font=DEFAULT_FONT, dpi=300)
    _save_to_file(tmpdir, p, c, 300, 'png')
    _save_to_file(tmpdir, p, c, 300, 'jpg')

    p = ChipPrinter(font=DEFAULT_FONT, dpi=600)
    _save_to_file(tmpdir, p, c, 600, 'png')
    _save_to_file(tmpdir, p, c, 600, 'jpg')
