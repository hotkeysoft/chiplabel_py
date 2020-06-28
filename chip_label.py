#!/usr/bin/env python3
from PIL import ImageFont, ImageDraw, Image
import math

DPI = 300 # pixels per inch
PIN_SPACING = 2.54 # in mm
NB_PINS = 28
#CHIP_WIDTH = 12 # in mm, 6 for narrow, 12 for wide
CHIP_WIDTH = 6 # in mm, 6 for narrow, 12 for wide
FONT_SIZE = 1.0 # desired font size in mm but not really, font size is not an exact science
INDENT_SIZE = 1.0 # in mm
FRAME = True

CHIP_NAME = 'ARDUINO328 Atmega328p with Adruino bootloader'
PINS = ['/RES', 'RX', 'TX', 'D2', 'D3', 'D4', 'VCC', 'GND', 'X1', 'X2', 'D5', 'D6', 'D7', 'D8',
        'D9', 'D10', 'D11', 'D12', 'D13', 'VCC', 'AREF', 'GND', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5']

def get_font_size() :
    height = FONT_SIZE * DPI / 25.4
    return math.ceil(height)

def get_indent_size():
    return math.ceil(INDENT_SIZE * DPI / 25.4)

def get_chip_size():
    width = CHIP_WIDTH * DPI / 25.4
    height = (NB_PINS//2) * PIN_SPACING * DPI / 25.4
    return (math.ceil(width), math.ceil(height))

def get_pin_y(pin):
    y = PIN_SPACING * (pin + 0.5) * DPI / 25.4
    return math.ceil(y)

def load_font(fontPath, size):
    font = ImageFont.truetype(fontPath, size)
    return font

def draw_frame(image):
    if FRAME:
        draw = ImageDraw.Draw(image)
        x,y = image.size
        draw.rectangle([(0,0), (x-1, y-1)])

def draw_pins(image, font):
    canvasX, canvasY = image.size
    draw = ImageDraw.Draw(image)

    rows = NB_PINS // 2
    pin = 0
    padding = 2 if FRAME else 0
    for col in range(2):
        for row in range(rows):
            y = get_pin_y(row)
            if (col == 1):
                y = canvasY-y
            pinName = PINS[pin]
            invert = pinName[0] in ('~', '/', '!')
            pinName = pinName[1:] if invert else pinName
            pin += 1
            textSizeX, textSizeY = draw.textsize(pinName, font=font)
            offsetY = math.ceil(textSizeY / 2.0)
            x = padding
            if col == 1:
                x = canvasX-textSizeX-padding
            draw.text((x, y-offsetY), pinName, font=font)
            if invert:
                draw.line([(x,y-offsetY), (x+textSizeX, y-offsetY)])

def draw_chipindent(image):
    _, canvasY = image.size
    indentPixels = get_indent_size()
    x0 = 0
    x1 = indentPixels
    y0 = (canvasY-indentPixels)//2
    y1 = y0 + indentPixels
    draw = ImageDraw.Draw(image)
    draw.line([(x0, y0), (x1//2, y0)])
    draw.line([(x0, y1), (x1//2, y1)])
    draw.arc([(x0, y0), (x1, y1)], 270, 90)

def draw_chipname(image, font):
    _, canvasY = image.size
    draw = ImageDraw.Draw(image)
    x0 = math.ceil(get_indent_size() * 1.2)

    _, textSizeY = draw.textsize(CHIP_NAME, font=font)
    draw.text((x0, (canvasY-textSizeY)//2), CHIP_NAME, font=font)

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

    image = Image.new(mode='1', size=canvas_size, color=255)
    #image = Image.new(mode='L', size=canvas_size, color=255)

    draw_frame(image)
    draw_pins(image, font)

    rotated = image.rotate(90, expand=True)

    draw_chipname(rotated, font)
    draw_chipindent(rotated)
    rotated.save("./out.png", dpi=(DPI, DPI))

    # if len(args) < 3:
    #     raise SystemExit(f'Usage: %s' % args[0])


if __name__ == '__main__':
    import sys
    main(sys.argv)
