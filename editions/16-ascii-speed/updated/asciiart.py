import argparse
import numpy as np
import subprocess
import csv
import pickle
from PIL import Image
from blessings import Terminal
import math

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python asciiart.py",
        usage="%(prog)s --file 'sample.jpg' -c -m 'lightness' -u -width 80 -scale 2",
        description="Print ASCII art to the terminal from image. If no file is specified, tries to take webcam image using imagesnap if installed."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        '-file', type=argparse.FileType('r'), 
        help='path to file to process (omit to use imagesnap)'                
    )
    parser.add_argument(
        '-color', action='store_true',
        help='render in glorious 256 bit color in supported environments!'
    )
    parser.add_argument(
        '-method', action='store', choices=['mean', 'lightness', 'luminosity'], default='lightness',
        help='method for calculating pixel density'
    )
    parser.add_argument(
        '-uninvert', action='store_true',
        help='uninvert pixel density (useful for light backgrounds)'
    )
    parser.add_argument(
        '-width', type=int, action='store', default=80,
        help='width of ASCII image before applying scaling width (default=80)'
    )
    parser.add_argument(
        '-scale', type=int, action='store', default=2, choices=range(1,4),
        help='scale width by factor of 1, 2, or 3 (default=2)'
    )
    return parser

# Create ANSI color dictionary
# Removed in favor of color dictionary saved in pickle
# with open('ansi_colors.csv') as file:
#     colors = list(csv.reader(file))
#     colors = colors[17:] # Remove header and reserved system colors (just use 16-255)
#     color_dict = {}
#     for color in colors:
#         color_dict[int(color[0])] = [int(color[2]), int(color[3]), int(color[4])]

# Return 2d list of values representing lightness, luminosity, or mean color
def single_value(array, method='mean'):
    if method == 'mean':
        single_value_array = array.mean(axis=2)
    elif method == 'lightness':
        single_value_array = (array.max(axis=2) + array.min(axis=2)) / 2
    elif method == 'luminosity':
        luminosity = lambda a : (a * np.array([.21, .72, .07])).sum()
        single_value_array = np.apply_along_axis(luminosity, 2, array)
    return single_value_array.tolist()

# Convert 0-255 value to ASCII character
def get_char(brightnessValue, invert):
    chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    step = 255/(len(chars) - 1)
    if invert:
        brightnessValue = 255 - brightnessValue
    return chars[round(brightnessValue / step)]

# Returned resized pixel array from image file
def initial_process(filename, new_width):
    with Image.open(filename) as im:
        new_height = round(new_width / im.size[1] * im.size[0])
        resized = im.resize((new_height, new_width))
        imarray = np.array(resized)
    return imarray

# Euclidean distance between two rgb values
def euclidean_distance(color1, color2):
    diff = lambda x, y: (y - x) ** 2
    distance = 0
    for value in range(3):
        distance += diff(color1[value], color2[value])
    return distance

# Find the closest ANSI color value by Euclidean distance
def closest_ANSI_color(color):
    color = color.tolist()
    distances = {}
    # Load ANSI color dictionary
    color_dict = pickle.load(open("ansi_color_dict.pkl", "rb"))
    for key in color_dict:
        distance = euclidean_distance(color_dict[key], color)
        distances[key] = distance
    return min(distances, key=distances.get)

# Create ANSI color mask from RGB image array
def color_mask(imarray, color_mapper):
    return np.apply_along_axis(color_mapper, 2, imarray)
    
# Take picture using imagesnap
def snapshot():
    try:
        subprocess.call(["imagesnap 'snapshot.jpg'"], shell=True)
    except:
        raise Exception("No file specified and imagesnap not available. See 'python asciiart.py --help'")

# 2d list of characters from 2d rgb array
def character_map(imarray, method, invert):
    value = single_value(imarray, method)
    return [[get_char(pixel, invert) for pixel in row] for row in value]

# Add ANSI color escapes to string
def string_color(ansi_value, string, on_color=16):
    term = Terminal()
    return term.on_color(on_color) + term.color(ansi_value) + string + term.normal

# Single color print to terminal
def print_to_terminal(list_of_lists, scale_row_by=2):
    print('\n')
    for row in list_of_lists:
        scaled_row = [scale_row_by * pixel for pixel in row]        
        print(''.join(scaled_row))

# Multicolor print to terminal        
def colors_print_to_terminal(character_map, color_array, scale_row_by=2):
    print('\n')
    for row_n, row in enumerate(character_map):
        scaled_row = ''
        for pixel_n, pixel in enumerate(row):
            pixel = string_color(color_array[row_n][pixel_n], pixel)
            scaled_row += (scale_row_by * pixel)
        print(''.join(scaled_row))

# We use the original author's `ansi_color_dict` that maps
# from ANSI color codes (eg. 23) to the RGB value
# represented by that code (eg. (0, 95, 95)). We
# invert it so that it maps from RGB => ANSI instead
# of ANSI => RGB. This allows us to easily answer
# the question "what is the ANSI value corresponding
# to this RGB value?"
#
# TODO: we shouldn't really do this in the body of the file.
# Tidying this up is left as an exercise for the reader.
color_dict = pickle.load(open("ansi_color_dict.pkl", "rb"))
inverted_color_dict = {}
for ansi, rgb in color_dict.items():
    inverted_color_dict[str(rgb)] = ansi

# Define gridlines using hexadecimal for ease of comparison
# with online resources.
GRIDLINES = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]

def rgb_to_ansi(rgb):
    def snap_value(val):
        return min(GRIDLINES, key=lambda el: abs(val - el))
    rgb = [snap_value(v) for v in rgb]
    return inverted_color_dict[str(rgb)]

def main():
    parser = init_argparse()
    args = parser.parse_args()
    if args.file == None:
        snapshot()
        filename = 'snapshot.jpg'
    else:
        args.file.close()
        filename = args.file.name
    imarray = initial_process(filename, args.width)
    invert = not args.uninvert
    character_array = character_map(imarray, args.method, invert)
    if args.color == True:
        color_array = color_mask(imarray, rgb_to_ansi)
        colors_print_to_terminal(character_array, color_array, args.scale)
    else:
        print_to_terminal(character_array, args.scale)

if __name__ == "__main__":
    main()

