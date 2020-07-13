# chiplabel_py
_chip_label.py_ generates customized labels with pin number for chips.

Quickstart
============
There are four modes (see [output examples below](#examples)):
- _image_ (default): generate a single image (.png) for each chip
  - `chip_label -c 555 7404 8085`
  - output: _555.png 7404.png 8085.png_
- _page_: generate one or more pages with all chips aligned in a grid
  - `chip_label -c 555 555 555 555 7404 7404 8085 -p`
  - output: _page1.png_ with all chips (4x555, 2x7404, 8085)
- _text_: output the chip pinout on stdout
  - `chip_label -c 555 -t`
  - output: ASCII pinout of the chip
- _list_: list all the chips in the library or libraries
  - `chip_label -l`

History
============
This project was inspired by [clabel](http://repetae.net/repos/clabel) (which is in Perl and can print on a PTouch label maker).
The original _clabel_ project repository was converted to git and [archived on github](https://github.com/hotkeysoft/chiplabel/tree/archive).

I started working on the original Perl code and made some [small improvements](https://github.com/hotkeysoft/chiplabel) but I decided to abandon the Perl version and start the whole thing from scratch in Python.

I kept the original YAML [configuration file format](#configuration-files) for the chips.

Requirements
============
- Python 3.6
- If you're not using the [installation package](#installation), you will need to install two libraries manually:
  - _PyYAML_ for parsing chip pinout files
    - simple install: `pip install PyYAML`
  - _Pillow_ for image generation and manipulation
    - simple install: `pip install Pillow`

or see [requirements.txt](requirements.txt)

Installation
============
### Manual Download
- Download or `git clone` sources
- Launch `chip_label.py` (or `python3 chip_label.py`) from project root
### Install Package with PIP
- Download latest release package
- Install with `pip3 install chiplabel-(version).tar.gz`
- If your paths are set properly you'll be able to launch `chip_label` from anywhere

Usage
============
```
usage: chip_label.py [-h] (-c name [name ...] | -a | -l) [-i dir] [-o dir] [-f font]
                     [--dpi num] [--invert] [-p] [--page_size n n] [--page_padding inch]
                     [--page_nocrop] [-t] [--debug | -v]

Generate footprint images for chips.

optional arguments:
  -h, --help            show this help message and exit
  -c name [name ...], --chip name [name ...]
                        one or more chip identifier
  -a, --all             generate labels for chips in package
  -l, --list            list all chips in package
  -i dir, --input dir   input chip library file or directory (default: $package/chips).
                        If a directory is specified all .yaml files in that directory
                        will be loaded
  -o dir, --output dir  output directory (default: .)
  --debug               print debugging statements
  -v, --verbose         print additional information

Image Options:
  -f font, --font font  TTF font to use (default: $package/fonts/CascadiaMono.ttf). Under
                        Windows the system font directory is searched automatically
  --dpi num             resolution in dots per inch (default: 300)
  --invert              invert label, for dead bug soldering

Page Mode Options:
  -p, --page            page mode: fit all specified chips in a grid on one or more pages
  --page_size n n       page width and height, in inches (default: 7.5 10)
  --page_padding inch   space between chips, in inches (default: 0.1)
  --page_nocrop         whitespace is cropped by default. Use this argument to leave the
                        whitespace

Text Output Options:
  -t, --text            generate text output in console instead of image. Image options
                        will be ignored
 ```
### @chiplist File

You can use a file with a list of chips (one chip per line) and pass it to the --chip parameter like this:
```chip_label -c @chiplist -p```

This will generate a page with all the chips in chiplist.  This if you are working on a project and want to label all the chips in it.  

In the _examples_ folder I put a file [beneater8bit.txt](./examples/beneater8bit.txt) that contains the BOM of the [Ben Eater's TTL Computer](https://eater.net/8bit)

I put the output of ```chip_label -c @examples/beneater8bit.txt -p``` [in the _out_ folder](./out/beneater8bit.png)

### Family Aliases
Chips part the 7400 family have auto-generated aliases (see [configuration file format](#configuration-files))

If your chip configuration file defines the 74999 chip, you will be able to generate chip images for all the variants:

```chip_label -c 74999 74LS999 74HCT999``` 

The only difference is the name printed on the chip.  This is useful to avoid mixing incompatible families by mistake.

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
- _family_: _7400_ generates family aliases for common (and uncommon) families: LS, ALS, HC, HCT, etc.

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
Future
============
- Multiple line pins
- Partial pin negation: R/(/W), /(B1) vs (/B)1
- Subscript A<sub>1</sub>
- Color output
