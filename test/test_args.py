#!/usr/bin/env python3
# test_args.py
import os
import pkg_resources
import pytest
from chiplabel import args

def test_no_args(capsys):
    with pytest.raises(SystemExit):
        args.parse_args([])

    captured = capsys.readouterr()
    assert 'usage:' in captured.err
    assert 'one of the arguments' in captured.err

def test_default_args():
    arg_list = args.parse_args(['-a'])

    assert arg_list.all == True
    assert arg_list.input.endswith('chips')
    assert os.path.isdir(arg_list.input)
    assert os.path.isdir(arg_list.output)
    assert arg_list.font.endswith('CascadiaMono.ttf')
    assert arg_list.dpi == 300
    assert arg_list.invert == False
    assert arg_list.page == False
    assert arg_list.page_size == [7.5, 10]
    assert arg_list.page_padding == 0.1
    assert arg_list.page_nocrop == False

def test_args():
    arg_list = args.parse_args([
        '-c', 'mychip',
        '-i', 'inputdir',
        '-o', 'outputdir',
        '-f', 'font',
        '--dpi', '234',
        '--invert',
        '-p',
        '--page_size', '5', '6',
        '--page_padding', '0.6',
        '--page_nocrop'
    ])

    assert arg_list.all == False
    assert arg_list.list == False
    assert arg_list.chip == ['mychip']
    assert arg_list.input == 'inputdir'
    assert arg_list.output == 'outputdir'
    assert arg_list.font == 'font'
    assert arg_list.dpi == 234
    assert arg_list.invert == True
    assert arg_list.page == True
    assert arg_list.page_size == [5.0, 6.0]
    assert arg_list.page_padding == 0.6
    assert arg_list.page_nocrop == True

def test_page_size_range(capsys):
    arg_list = args.parse_args(['-a', '--page_size', '1', '1'])
    assert arg_list.page_size == [1.0, 1.0]

    arg_list = args.parse_args(['-a', '--page_size', '20', '20'])
    assert arg_list.page_size == [20.0, 20.0]    

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '--page_size', '0.5', '1'])
    capture = capsys.readouterr()                
    assert 'argument --page_size: 0.5' in capture.err

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '--page_size', '1', '0.6'])
    capture = capsys.readouterr()        
    assert 'argument --page_size: 0.6' in capture.err

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '--page_size', '1', 'badsize'])
    capture = capsys.readouterr()        
    assert 'argument --page_size: badsize' in capture.err       

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '--page_size', '1'])
    capture = capsys.readouterr()        
    assert 'argument --page_size: expected 2 arguments' in capture.err       

def test_page_padding_range(capsys):
    arg_list = args.parse_args(['-a', '--page_padding', '0'])
    assert arg_list.page_padding == 0

    arg_list = args.parse_args(['-a', '--page_padding', '1'])
    assert arg_list.page_padding == 1

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '--page_padding', '-0.1'])
    capture = capsys.readouterr()                
    assert 'argument --page_padding: -0.1' in capture.err

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '--page_padding', '1.1'])
    capture = capsys.readouterr()        
    assert 'argument --page_padding: 1.1' in capture.err

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '--page_padding', 'badpad'])
    capture = capsys.readouterr()        
    assert 'argument --page_padding: badpad' in capture.err       

def test_dpi_range(capsys):
    arg_list = args.parse_args(['-a', '--dpi', '100'])
    assert arg_list.dpi == 100

    arg_list = args.parse_args(['-a', '--dpi', '2000'])
    assert arg_list.dpi == 2000

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '--dpi', '99'])
    capture = capsys.readouterr()                
    assert 'argument --dpi: 99' in capture.err

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '--dpi', '2001'])
    capture = capsys.readouterr()        
    assert 'argument --dpi: 2001' in capture.err

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '--dpi', 'baddpi'])
    capture = capsys.readouterr()        
    assert 'argument --dpi: baddpi' in capture.err       

def test_mode(capsys):
    arg_list = args.parse_args(['-a'])
    assert arg_list.all == True
    assert arg_list.list == False
    assert arg_list.chip == None

    arg_list = args.parse_args(['-l'])
    assert arg_list.all == False
    assert arg_list.list == True
    assert arg_list.chip == None

    arg_list = args.parse_args(['-c', 'chip'])
    assert arg_list.all == False
    assert arg_list.list == False
    assert arg_list.chip == ['chip']

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '-l'])
    capture = capsys.readouterr()        
    assert 'not allowed with argument' in capture.err

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-a', '-c', 'chip'])
    capture = capsys.readouterr()        
    assert 'not allowed with argument' in capture.err

    with pytest.raises(SystemExit):
        arg_list = args.parse_args(['-l', '-c', 'chip'])
    capture = capsys.readouterr()        
    assert 'not allowed with argument' in capture.err
