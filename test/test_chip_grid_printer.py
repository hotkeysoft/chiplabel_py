#!/usr/bin/env python3
# test_chip_grid_printer.py

import pkg_resources
import pytest
from PIL import Image
from PIL import ImageChops
from chiplabel import chip
from chiplabel.chip_grid_printer import ChipGridPrinter

CREATE_REFERENCES = False
FONT_DIR = pkg_resources.resource_filename('chiplabel', 'fonts')
DEFAULT_FONT = f'{FONT_DIR}/CascadiaMono.ttf'
REF_DIR = pkg_resources.resource_filename('test', 'data/img')

def test_init():
    c = ChipGridPrinter()
    assert c.config['dpi'] == 300
    assert c.config['invert'] == False
    assert c.config['font'] == ''
    assert c.font
    assert c.dpi == 300    
    assert c.page_padding == 0.1
    assert c.page_padding_pixels == 30
    assert c.page_size == (1, 1)
    assert c.page_size_pixels == (300, 300)

    c = ChipGridPrinter(invert=True, foo='bar', dpi=600, 
        page_size=(4, 4), page_padding=0.2)
    assert c.config['invert'] == True
    assert c.config['foo'] == 'bar'
    assert c.font
    assert c.dpi == 600
    assert c.page_padding == 0.2
    assert c.page_padding_pixels == 120
    assert c.page_size == (4, 4)    
    assert c.page_size_pixels == (2400, 2400)

# 2x2 chips/page
def test_print_to_page(tmpdir):    
    c = chip.Chip('id', 20, rowSpacing=25.4)

    # Square page
    p = ChipGridPrinter(page_size=(2, 2), 
        page_padding=0, output=tmpdir)
    assert p.page_size_pixels == (600, 600)

    # Square chip
    chip_size = p.get_chip_size(c)
    assert chip_size == (300, 300)

    assert p.current_page == 1
    assert p.page_pos == (0, 0)

    # Row 0
    p.print_to_page(c)
    assert p.current_page == 1
    assert p.page_pos == (300, 0)

    p.print_to_page(c)
    assert p.current_page == 1
    assert p.page_pos == (600, 0)

    # Row 1
    p.print_to_page(c)
    assert p.current_page == 1
    assert p.page_pos == (300, 300)

    p.print_to_page(c)
    assert p.current_page == 1
    assert p.page_pos == (600, 300)

    # Page 2
    p.print_to_page(c)
    assert p.current_page == 2
    assert p.page_pos == (300, 0)

    assert tmpdir.join('page1.png').check(file=1)
    # Page 2 is not complete, need to save manually
    assert tmpdir.join('page2.png').check(file=0)
    p.save_page()
    assert tmpdir.join('page2.png').check(file=1)

# With padding, 1x1 chip / page
def test_print_to_page2(tmpdir):    
    c = chip.Chip('id', 20, rowSpacing=25.4)

    # Square page
    p = ChipGridPrinter(page_size=(2, 2), 
        page_padding=0.1, output=tmpdir)
    assert p.page_size_pixels == (600, 600)
    assert p.page_padding_pixels == 30

    # Square chip
    chip_size = p.get_chip_size(c)
    assert chip_size == (300, 300)

    assert p.current_page == 1
    assert p.page_pos == (0, 0)

    # Row 0
    p.print_to_page(c)
    assert p.current_page == 1
    assert p.page_pos == (330, 0)

    # Page 2
    p.print_to_page(c)
    assert p.current_page == 2
    assert p.page_pos == (330, 0)

    # Page 3
    p.print_to_page(c)
    assert p.current_page == 3
    assert p.page_pos == (330, 0)

    assert tmpdir.join('page1.png').check(file=1)
    assert tmpdir.join('page2.png').check(file=1)
    # Page 3 is not complete, need to save manually
    assert tmpdir.join('page3.png').check(file=0)
    p.save_page()
    assert tmpdir.join('page3.png').check(file=1)

# With padding, 2x2 chip / page
def test_print_to_page3(tmpdir):    
    c = chip.Chip('id', 20, rowSpacing=25.4)

    # Square page
    p = ChipGridPrinter(page_size=(2.2, 2.2), 
        page_padding=0.1, output=tmpdir)
    assert p.page_size_pixels == (660, 660)
    assert p.page_padding_pixels == 30

    # Square chip
    chip_size = p.get_chip_size(c)
    assert chip_size == (300, 300)

    assert p.current_page == 1
    assert p.page_pos == (0, 0)

    # Row 0
    p.print_to_page(c)
    assert p.current_page == 1
    assert p.page_pos == (330, 0)

    p.print_to_page(c)
    assert p.current_page == 1
    assert p.page_pos == (660, 0)

    # Row 1
    p.print_to_page(c)
    assert p.current_page == 1
    assert p.page_pos == (330, 330)

    p.print_to_page(c)
    assert p.current_page == 1
    assert p.page_pos == (660, 330)

    # Page 2
    p.print_to_page(c)
    assert p.current_page == 2
    assert p.page_pos == (330, 0)

    assert tmpdir.join('page1.png').check(file=1)
    # Page 3 is not complete, need to save manually
    assert tmpdir.join('page2.png').check(file=0)
    p.save_page()
    assert tmpdir.join('page2.png').check(file=1)

def test_new_page(tmpdir):    
    c = chip.Chip('id', 20, rowSpacing=25.4)

    # Square page
    p = ChipGridPrinter(page_size=(2.2, 2.2), 
        page_padding=0.1, output=tmpdir)
    assert p.page_size_pixels == (660, 660)
    assert p.page_padding_pixels == 30

    # Square chip
    chip_size = p.get_chip_size(c)
    assert chip_size == (300, 300)

    assert p.current_page == 1
    assert p.page_pos == (0, 0)

    # Row 0
    p.print_to_page(c)
    assert p.current_page == 1
    assert p.page_pos == (330, 0)

    p.save_page()
    p.new_page()
    assert p.current_page == 2
    assert p.page_pos == (0, 0)

    p.print_to_page(c)
    assert p.current_page == 2
    assert p.page_pos == (330, 0)

    assert tmpdir.join('page1.png').check(file=1)
    # Page 3 is not complete, need to save manually
    assert tmpdir.join('page2.png').check(file=0)
    p.save_page()
    assert tmpdir.join('page2.png').check(file=1)

# With padding, 2x2 chip / page
def test_print_chips(tmpdir):    
    c = chip.Chip('id', 20, rowSpacing=25.4)

    # Square page
    p = ChipGridPrinter(page_size=(2.2, 2.2), 
        page_padding=0.1, output=tmpdir)
    assert p.page_size_pixels == (660, 660)
    assert p.page_padding_pixels == 30

    # Square chip
    chip_size = p.get_chip_size(c)
    assert chip_size == (300, 300)

    assert p.current_page == 1
    assert p.page_pos == (0, 0)

    p.print_chips([c]*15)

    assert p.current_page == 4
    assert p.page_pos == (330, 330)

    assert tmpdir.join('page1.png').check(file=1)
    assert tmpdir.join('page2.png').check(file=1)
    assert tmpdir.join('page3.png').check(file=1)
    assert tmpdir.join('page4.png').check(file=1)

def test_output_dir():    
    c = chip.Chip('id', 20)
    p = ChipGridPrinter(output='bad/dir')
    with pytest.raises(ValueError):
        p.save_page()
