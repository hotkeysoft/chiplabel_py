#!/usr/bin/env python3
# test_chip_grid_printer.py

import pkg_resources
import pytest
from chiplabel import chip_label

TEST_DIR = pkg_resources.resource_filename('test', 'data')

# List default input dir
def test_list_default(capsys):
    args = ['', '-l']    
    chip_label.main(args)

    captured = capsys.readouterr()    
    assert '7400/7402\n' in captured.out
    assert 'sound/SN76489AN\n' in captured.out
    assert 'pld/DTBANK1\n' in captured.out
    assert 'cpu/8085\n' in captured.out

def test_list_nofile(capsys):
    args = ['', '-l', '-i', f'{TEST_DIR}/chip.notfound']
    chip_label.main(args)
    captured = capsys.readouterr()    
    assert 'ERROR' in captured.err
    assert 'loading chip list' in captured.err

def test_list_single(capsys):
    args = ['', '-l', '-i', f'{TEST_DIR}/chip2.yaml']
    chip_label.main(args)

    captured = capsys.readouterr()    
    assert 'chip2/555\n' in captured.out
    assert 'chip2/TestChip\n' in captured.out

def test_list_dir(capsys):
    args = ['', '-l', '-i', f'{TEST_DIR}']
    chip_label.main(args)

    captured = capsys.readouterr()    
    assert 'chip1/555\n' in captured.out
    assert 'chip2/555\n' in captured.out
    assert 'chip2/TestChip\n' in captured.out

def test_bad_output_dir(capsys):
    args = ['', '-c', 'TestChip', 
        '-i', f'{TEST_DIR}', 
        '-o', f'{TEST_DIR}/baddir']
    chip_label.main(args)
    captured = capsys.readouterr()    
    assert 'ERROR' in captured.err
    assert 'directory not found' in captured.err

def test_all_from_directory(tmpdir, capsys):
    args = ['', '-a',
        '-i', f'{TEST_DIR}', 
        '-o', str(tmpdir)]
    chip_label.main(args)
    captured = capsys.readouterr()    
    assert 'ERROR' not in captured.err

    assert tmpdir.join('555.png').check(file=1)    
    assert tmpdir.join('TestChip.png').check(file=1)
  
def test_all_from_file(tmpdir, capsys):
    args = ['', '-a',
        '-i', f'{TEST_DIR}/chip1.yaml', 
        '-o', str(tmpdir)]
    chip_label.main(args)
    captured = capsys.readouterr()    
    assert 'ERROR' not in captured.err

    assert tmpdir.join('555.png').check(file=1)    
    assert tmpdir.join('TestChip.png').check(file=0)

def test_chip_from_file(tmpdir, capsys):
    args = ['', '-c', '555',
        '-i', f'{TEST_DIR}/chip1.yaml', 
        '-o', str(tmpdir)]
    chip_label.main(args)
    captured = capsys.readouterr()    
    assert 'ERROR' not in captured.err

    assert tmpdir.join('555.png').check(file=1)    
    assert tmpdir.join('TestChip.png').check(file=0)

def test_chip_notfound_from_file(tmpdir, capsys):
    args = ['', '-c', '444',
        '-i', f'{TEST_DIR}/chip1.yaml', 
        '-o', str(tmpdir)]
    chip_label.main(args)
    captured = capsys.readouterr()    
    assert 'WARNING' in captured.err
    assert 'Chip not found' in captured.err
    assert 'Nothing to do' in captured.err

    assert tmpdir.join('444.png').check(file=0)
    assert tmpdir.join('555.png').check(file=0)
    assert tmpdir.join('TestChip.png').check(file=0)

def test_chip_multi_from_file(tmpdir, capsys):
    args = ['', '-c', '444', '555',
        '-i', f'{TEST_DIR}/chip1.yaml', 
        '-o', str(tmpdir)]
    chip_label.main(args)
    captured = capsys.readouterr()    
    assert 'WARNING' in captured.err
    assert 'Chip not found' in captured.err
    assert 'Nothing to do' not in captured.err

    assert tmpdir.join('444.png').check(file=0)
    assert tmpdir.join('555.png').check(file=1)
    assert tmpdir.join('TestChip.png').check(file=0)

def test_text_output(capsys):
    args = ['', '-t', '-c', '444', '555']
    chip_label.main(args)
    captured = capsys.readouterr()    
    assert 'WARNING' in captured.err
    assert 'Chip not found' in captured.err
    assert '555' in captured.out
    assert '444' not in captured.out

def test_all_page_from_directory(tmpdir, capsys):
    args = ['', '-a', '-p',
        '-i', f'{TEST_DIR}', 
        '-o', str(tmpdir)]
    chip_label.main(args)
    captured = capsys.readouterr()    
    assert 'ERROR' not in captured.err
    assert tmpdir.join('page1.png').check(file=1)    

def test_verbose(capsys):
    args = ['', '-v', '-t', '-c', '555']
    chip_label.main(args)
    captured = capsys.readouterr()    
    assert 'Found 1 chips' in captured.err
    assert 'Printing 1 chips to text' in captured.err
    assert '555 Timer' in captured.out
