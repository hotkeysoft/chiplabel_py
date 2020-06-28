#!/usr/bin/env python3
from PIL import ImageFont, ImageDraw, Image
import math

DPI = 300 # pixels per inch
PIN_SPACING = 2.54 # in mm
NB_PINS = 24
CHIP_WIDTH = 12 # in mm, 6 for narrow, 12 for wide
FONT_SIZE = 1.5 # desired font size in mm but not really, font size is not an exact science

def get_font_size() :
    height = FONT_SIZE * DPI / 25.4
    return math.ceil(height)

def get_chip_size() :
    width = CHIP_WIDTH * DPI / 25.4
    height = (NB_PINS//2) * PIN_SPACING * DPI / 25.4
    return (math.ceil(width), math.ceil(height))

def get_pin_y(pin) :
    y = PIN_SPACING * (pin + 0.5) * DPI / 25.4
    return math.ceil(y)

def load_font(fontPath, size) :
    font = ImageFont.truetype(fontPath, size)
    return font

def draw_pins(draw, font, size) :
    rows = NB_PINS // 2

    #draw.textsize("world", font=font)

    pin = 0
    for col in range(2):
        for row in range(rows):
            pin += 1
            y = get_pin_y(row)
            pinName = f'PIN{pin}'
            textSize = draw.textsize(pinName, font=font)
            offsetY = math.ceil(textSize[1] / 2.0)
            x = 0
            if col == 1:
                x = size[0]-textSize[0]
            #draw.line([(x,y), (x+textSize[0],y)])
            draw.text((x, y-offsetY), pinName, font=font)

def main(args):
    import logging
    logging.basicConfig(
        filename = 'chip_label.log',
        filemode = 'w',
        level = logging.DEBUG
    )

    font_size = get_font_size()
    print("font size ", font_size)
    font = load_font('fonts/CascadiaMono.ttf', font_size)

    canvas_size = get_chip_size()
    print("canvas size ", canvas_size)

    image = Image.new(mode='L', size=canvas_size, color=255)

    draw = ImageDraw.Draw(image)

    draw_pins(draw, font, canvas_size)

    image.save("./out.png", dpi=(DPI, DPI))

    # if len(args) < 3:
    #     raise SystemExit(f'Usage: %s' % args[0])


if __name__ == '__main__':
    import sys
    main(sys.argv)
