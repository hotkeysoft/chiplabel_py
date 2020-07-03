# chiplabel_py
_chip_label.py_ generates customized labels with pin number for chips.

This project was inspired by [clabel](http://repetae.net/repos/clabel) (which is in Perl and can print on a PTouch label maker).
The original _clabel_ project repository was converted to git and [archived on github](https://github.com/hotkeysoft/chiplabel/tree/archive).

I started working on the original Perl code and made some [small improvements](https://github.com/hotkeysoft/chiplabel) but I decided to abandon the Perl version and start the whole thing from scratch in Python.

I kept the original YAML [configuration file format](#configuration-files) for the chips.

Requirements
============
- Python 3.6
- _PyYAML_ for parsing chip pinout files
  - simple install: `pip install PyYAML`
- _Pillow_ for image generation and manipulation
  - simple install: `pip install Pillow`

or see [requirements.txt](requirements.txt)

Usage
============
```
usage: chip_label.py [-h] (-c name [name ...] | -a | -l) [-i dir] [-o dir] [-f font]
                     [--dpi num] [--invert] [-p] [--page_size n n] [--page_padding inch]
                     [-t] [--debug | -v]

Generate footprint images for chips.

optional arguments:
  -h, --help            show this help message and exit
  -c name [name ...], --chip name [name ...]
                        one or more chip identifier
  -a, --all             generate labels for chips in package
  -l, --list            list all chips in package
  -i dir, --input dir   input chip library file or directory (default: ./chips). If a
                        directory is specified all .yaml files in that directory will be
                        loaded
  -o dir, --output dir  output directory (default: ./out)
  --debug               print debugging statements
  -v, --verbose         print additional information

Image Options:
  -f font, --font font  TTF font to use (default: ./fonts/CascadiaMono.ttf). Under Windows
                        the system font directory is searched automatically
  --dpi num             resolution in dots per inch (default: 300)
  --invert              invert label, for dead bug soldering

Page Mode Options:
  -p, --page            page mode: fit all specified chips in a grid on one or more pages
  --page_size n n       page width and height, in inches (default: 7.5 10)
  --page_padding inch   space between chips, in inches (default: 0.1)

Text Output Options:
  -t, --text            generate text output in console instead of image. Image options will
                        be ignored
 ```
Examples
============
### Image Output (default)
#### 555 timer IC
![555 timer IC example](https://github.com/hotkeysoft/chiplabel_py/raw/master/out/555.png "sample output: 555 timer")

#### 8085 CPU
![8085 CPU example](https://github.com/hotkeysoft/chiplabel_py/raw/master/out/8085.png "sample output: 8085 CPU")

### Text Output (_-t_ parameter)
```
SN76489AN Sound Generator
   -----------
 1 | D5  VCC | 16
 2 | D6   D4 | 15
 3 | D7  CLK | 14
 4 | RDY  D3 | 13
 5 | /WE  D2 | 12
 6 | /CE  D1 | 11
 7 | OUT  D0 | 10
 8 | GND  NC | 9
   -----------
```
Configuration files
============
A _chip library_ configuration file is a .yaml file containing a list of chip definition such as:
```YAML
SN76489AN:
    description: Sound Generator
    pins: [ D5, D6, D7, RDY, /WE, /CE, OUT, GND, NC, D0, D1, D2, D3, CLK, D4, VCC ]
```
The format is very simple as you can see.  The only required fields are the chip id (e.g. _SN76489AN_ in the example above) and the list of pins.

The optional fields are:
- _name_: replaces the chip id on the label.
- _description_: appended to name.
- _type_: _wide_ generates 12mm labels instead of the default 6mm.

### Advanced Configuration
#### Inverted pin
Pins that start with '/', '!' or '~' will be drawn as inverted (with a line on top):
  - /OE
  - !WR
  - ~RD

These are functionally equivalent.

#### Hidden Chips, Templates
Chips with an id that begins with an underscore (\_) are hidden from chip list. This is useful to generate many chips based on the same pinout without cluttering the chip list:

```YAML
_op1: &op1
  description: OpAmp
  pins: [BAL, IN-, IN+, V-, BAL, OUT, V+, NC]

  LF356: *op1
  LM741: *op1
```
This will generate two chips with the same pinout: LF356 and LM741.  You can override fields (such as description) like this:
```YAML
LM741:
  <<: *op1  
  description: custom description
```
