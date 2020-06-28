# chiplabel_py
Remake of chiplabel in python, work in progress

Inspired by [clabel project](http://repetae.net/repos/clabel)

The project is also [archived on github](https://github.com/hotkeysoft/chiplabel/tree/archive)

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
usage: chip_label.py [-h] (-c name | -a | -l) [-o dir]

Generate footprint images for chips

optional arguments:
  -h, --help            show this help message and exit
  -c name, --chip name  chip identifier
  -a, --all             generate labels for chips in package
  -l, --list            list all chips in package
  -o dir, --output dir  output directory (default: ./out)
  -f file, --font file  ttf font to use (default: ./fonts/CascadiaMono.ttf). Under Windows the system font directory
                        is searched automatically.
  -d num, --dpi num     resolution in dots per inch (default: 300)  
 ```
Examples
============
### 555 timer IC
![555 timer IC example](https://github.com/hotkeysoft/chiplabel_py/raw/master/out/555.png "sample output: 555 timer")

### 8085 CPU
![8085 CPU example](https://github.com/hotkeysoft/chiplabel_py/raw/master/out/8085.png "sample output: 8085 CPU")
