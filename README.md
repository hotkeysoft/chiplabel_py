# chiplabel_py
_chip_label.py_ generates customized labels with pin number for chips.

This project was inspired by [clabel](http://repetae.net/repos/clabel) (which is in Perl and can print on a PTouch label maker).
The original _clabel_ project repository was converted to git and [archived on github](https://github.com/hotkeysoft/chiplabel/tree/archive).

I started working on the original Perl code and made some [small improvements](https://github.com/hotkeysoft/chiplabel) but I decided to abandon the Perl version and start the whole thing from scratch in Python.

I kept the original YAML [configuration file format](#configuration-files) for the chips.

Requirements
============
- Needs PyYAML for parsing chip pinout files
  - simple install: `pip install PyYAML`
- Needs Pillow for image generation and manipulation
  - simple install: `pip install Pillow`

or see [requirements.txt](requirements.txt)

Usage
============
```
usage: chip_label.py [-h] (-c name | -a | -l) [-o dir] [-f file] [-d num] [-i] [--debug | -v]

Generate footprint images for chips.

optional arguments:
  -h, --help            show this help message and exit
  -c name, --chip name  Chip identifier.
  -a, --all             Generate labels for chips in package.
  -l, --list            List all chips in package.
  -i dir, --input dir   Input chip library file or directory (default: ./chips). If a directory
                        is specified all .yaml files in that directory will be loaded.  
  -o dir, --output dir  Output directory (default: ./out).
  -f file, --font file  TTF font to use (default: ./fonts/CascadiaMono.ttf). Under Windows the
                        system font directory is searched automatically.
  -d num, --dpi num     Resolution in dots per inch (default: 300).
  -i, --invert          Invert label, for dead bug soldering.
  --debug               Print debugging statements.
  -v, --verbose         Print additional information.
 ```
Examples
============
### 555 timer IC
![555 timer IC example](https://github.com/hotkeysoft/chiplabel_py/raw/master/out/555.png "sample output: 555 timer")

### 8085 CPU
![8085 CPU example](https://github.com/hotkeysoft/chiplabel_py/raw/master/out/8085.png "sample output: 8085 CPU")

Configuration files
============
A _chip library_ configuration file is a .yaml file containing a list of chip definition such as:
```YAML
SN76489AN:
    name: Sound Generator
    pins: [ D5, D6, D7, RDY, /WE, /CE, OUT, GND, NC, D0, D1, D2, D3, CLK, D4, VCC ]
```
The format is very simple as you can see.  The only required fields are the chip id (e.g. _SN76489AN_ in the example above) and the list of pins.

The optional fields are:
- _name_: more of a description field, will be appended to the chip id on the label
- _type: wide_ generates 12mm labels instead of the default 6mm

At the moment the only chip library configuration file loaded is [chips/chips.yaml](https://github.com/hotkeysoft/chiplabel_py/blob/master/chips/chips.yaml).
This will be customizable eventually.
