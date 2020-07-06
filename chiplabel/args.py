#!/usr/bin/env python3
import argparse
import logging
import pkg_resources
log = logging.getLogger(__name__)

MIN_DPI = 100
MAX_DPI = 2000
DEFAULT_DPI = 300
DEFAULT_FONT = 'CascadiaMono.ttf'
DEFAULT_FONT_DIR = pkg_resources.resource_filename('chiplabel', f'fonts/{DEFAULT_FONT}')
DEFAULT_INPUT_DIR = pkg_resources.resource_filename('chiplabel', 'chips')
DEFAULT_OUTPUT_DIR = '.'

MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 20
DEFAULT_PAGE_SIZE = [7.5, 10]

MIN_PADDING = 0
MAX_PADDING = 1
DEFAULT_PAGE_PADDING = 0.1

def _page_padding_range(string):
    try:
        value = float(string)
        if value < MIN_PADDING or value > MAX_PADDING:
            raise argparse.ArgumentTypeError(f'{value} is not in range [{MIN_PADDING}, {MAX_PADDING}]')
    except ValueError:
        raise argparse.ArgumentTypeError(f'{string} is not an integer value')
    return value

def _page_size_range(string):
    try:
        value = float(string)
        if value < MIN_PAGE_SIZE or value > MAX_PAGE_SIZE:
            raise argparse.ArgumentTypeError(f'{value} is not in range [{MIN_PAGE_SIZE}, {MAX_PAGE_SIZE}]')
    except ValueError:
        raise argparse.ArgumentTypeError(f'{string} is not an integer value')
    return value

def _dpi_range(string):
    try:
        value = int(string)
        if value < MIN_DPI or value > MAX_DPI:
            raise argparse.ArgumentTypeError(f'{value} is not in range [{MIN_DPI}, {MAX_DPI}]')
    except ValueError:
        raise argparse.ArgumentTypeError(f'{string} is not an integer value')
    return value

def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Generate footprint images for chips.', 
        fromfile_prefix_chars='@'
    )

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        '-c', '--chip',
        nargs='+',
        metavar='name',
        help='one or more chip identifier'
    )
    action_group.add_argument(
        '-a', '--all',
        help='generate labels for chips in package',
        action='store_true'
    )
    action_group.add_argument(
        '-l', '--list',
        help='list all chips in package',
        action='store_true'
    )

    parser.add_argument(
        '-i', '--input',
        metavar='dir',
        help='input chip library file or directory (default: $package/chips). If a directory is specified all .yaml files in that directory will be loaded',
        default=DEFAULT_INPUT_DIR
    )
    parser.add_argument(
        '-o', '--output',
        metavar='dir',
        help=f'output directory (default: {DEFAULT_OUTPUT_DIR})',
        default=DEFAULT_OUTPUT_DIR
    )

    graph_group = parser.add_argument_group('Image Options')
    graph_group.add_argument(
        '-f', '--font',
        metavar='font',
        help=f'TTF font to use (default: $package/fonts/{DEFAULT_FONT}). Under Windows the system font directory is searched automatically',
        default=DEFAULT_FONT_DIR
    )
    graph_group.add_argument(
        '--dpi',
        metavar='num',
        type=_dpi_range,
        help=f'resolution in dots per inch (default: {DEFAULT_DPI})',
        default=DEFAULT_DPI
    )
    graph_group.add_argument(
        '--invert',
        help='invert label, for dead bug soldering',
        action='store_true'
    )

    page_group = parser.add_argument_group('Page Mode Options')
    page_group.add_argument(
        '-p', '--page',
        help='page mode: fit all specified chips in a grid on one or more pages',
        action='store_true'
    )
    page_group.add_argument(
        '--page_size',
        nargs=2,
        metavar='n',
        type=_page_size_range,
        help=f'page width and height, in inches (default: {DEFAULT_PAGE_SIZE[0]} {DEFAULT_PAGE_SIZE[1]})',
        default=DEFAULT_PAGE_SIZE
    )
    page_group.add_argument(
        '--page_padding',
        metavar='inch',
        type=_page_padding_range,
        help=f'space between chips, in inches (default: {DEFAULT_PAGE_PADDING})',
        default=DEFAULT_PAGE_PADDING
    )

    page_group.add_argument(
        '--page_nocrop',
        action='store_true',
        help='whitespace is cropped by default. Use this argument to leave the whitespace',
    )

    text_group = parser.add_argument_group('Text Output Options')

    text_group.add_argument(
        '-t', '--text',
        help=f'generate text output in console instead of image.  Image options will be ignored',
        action="store_true"
    )

    debug_group = parser.add_mutually_exclusive_group()
    debug_group.add_argument(
        '--debug',
        help="print debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    debug_group.add_argument(
        '-v', '--verbose',
        help="print additional information",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    return parser.parse_args(args)