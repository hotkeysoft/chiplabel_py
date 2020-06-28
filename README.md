# chiplabel_py
Remake of chiplabel in python, work in progress

Inspired by [clabel project](http://repetae.net/repos/clabel)

The project is also [archived on github](https://github.com/hotkeysoft/chiplabel/tree/archive)

## Requirements
- Needs PyYAML for parsing chip pinout files
  - simple install: `pip install PyYAML`
- Needs Pillow for image generation and manipulation
  - simple install: `pip install Pillow`

or see [requirements.txt](requirements.txt)

## Usage
```
usage: chip_label.py [-h] (-c name | -a | -l) [-o dir]

Generate footprint images for chips

optional arguments:
  -h, --help            show this help message and exit
  -c name, --chip name  chip identifier
  -a, --all             generate labels for chips in package
  -l, --list            list all chips in package
  -o dir, --output dir  output directory (default: ./out)
 ```
