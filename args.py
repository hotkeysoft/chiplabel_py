#!/usr/bin/env python3
import argparse
import logging
log = logging.getLogger(__name__)

MIN_DPI = 50
MAX_DPI = 2000
DEFAULT_DPI = 300

DEFAULT_FONT = './fonts/CascadiaMono.ttf'
DEFAULT_INPUT_DIR = './chips'
DEFAULT_OUTPUT_DIR = './out'

def _dpi_range(string):
    try:
        value = int(string)
        if value < MIN_DPI or value > MAX_DPI:
            raise argparse.ArgumentTypeError(f'{value} is not in range [{MIN_DPI}, {MAX_DPI}]')
    except ValueError:
        raise argparse.ArgumentTypeError(f'{string} is not an integer value')
    return value

def parse_args():
    parser = argparse.ArgumentParser(description='Generate footprint images for chips.')

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        '-c', '--chip',
        nargs='+',
        metavar='name',
        help='One or more chip identifier.'
    )
    action_group.add_argument(
        '-a', '--all',
        help='Generate labels for chips in package.',
        action='store_true'
    )
    action_group.add_argument(
        '-l', '--list',
        help='List all chips in package.',
        action='store_true'
    )

    parser.add_argument(
        '-i', '--input',
        metavar='dir',
        help=f'Input chip library file or directory (default: {DEFAULT_INPUT_DIR}). If a directory is specified all .yaml files in that directory will be loaded.',
        default=DEFAULT_INPUT_DIR
    )
    parser.add_argument(
        '-o', '--output',
        metavar='dir',
        help=f'Output directory (default: {DEFAULT_OUTPUT_DIR}).',
        default=DEFAULT_OUTPUT_DIR
    )

    graph_group = parser.add_argument_group('Image Options')
    graph_group.add_argument(
        '-f', '--font',
        metavar='font',
        help=f'TTF font to use (default: {DEFAULT_FONT}). Under Windows the system font directory is searched automatically.',
        default=DEFAULT_FONT
    )
    graph_group.add_argument(
        '--dpi',
        metavar='num',
        type=_dpi_range,
        help=f'Resolution in dots per inch (default: {DEFAULT_DPI}).',
        default=DEFAULT_DPI
    )
    graph_group.add_argument(
        '--invert',
        help='Invert label, for dead bug soldering.',
        action='store_true'
    )
    graph_group.add_argument(
        '-p', '--page',
        help='Page mode: fit all specified chips in a grid on one or more pages.',
        action='store_true'
    )

    parser.add_argument(
        '-t', '--text',
        help=f'Generate text output in console instead of image.  Image options will be ignored.',
        action="store_true"
    )

    debug_group = parser.add_mutually_exclusive_group()

    debug_group.add_argument(
        '--debug',
        help="Print debugging statements.",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    debug_group.add_argument(
        '-v', '--verbose',
        help="Print additional information.",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    return parser.parse_args()