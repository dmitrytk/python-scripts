#!/usr/bin/env python
"""
Convert coordinates between projections
Get data from clipboard. Result copied to clipboard.
data format (TAB field separator):
60.56   70.12
60.57   45.46
Usage:
./proj.py in_proj out_proj [-o deg]
[-o deg] - optional degree conversion: 60.265 -> 60 15 54.60
List of projections in PROJECTIONS dictionary
"""

import argparse
import re
from math import ceil, floor

import pyperclip
from pyproj import Transformer

from runner import run


def deg2dec(data):
    """Convert  <str> 60 15 54.60 ->  <float> 60.265"""

    d, m, s = tuple([float(i) for i in data.split(' ')])
    if d < 0:
        return str(d - m / 60 - s / 3600)
    return str(d + m / 60 + s / 3600)


def dec2deg(data):
    """Convert  float 60.265 ->  str 60 15 54.60"""

    decimal = float(data)
    positive = decimal > 0
    degree = floor(decimal) if positive else ceil(decimal)
    minute = floor((decimal - degree) *
                   60) if positive else floor((degree - decimal) * 60)
    second = round((decimal - degree - minute / 60) * 3600,
                   2) if positive else round((degree - decimal - minute / 60) * 3600, 2)
    # Add leading zero if < 10
    degree = f'0{degree}' if degree < 10 else degree
    minute = f'0{minute}' if minute < 10 else minute
    second = f'0{second}' if second < 10 else second
    return f'{degree} {minute} {second}'


# Command line args
# in_proj and out_proj required
parser = argparse.ArgumentParser(description='Videos to images')
parser.add_argument('in_proj', type=str, help='Input projection')
parser.add_argument('out_proj', type=str, help='Output projection')
parser.add_argument('-o', action="store", dest="out_deg")
args = parser.parse_args()
out_deg = args.out_deg == 'deg'

# Projections
PROJECTIONS = {
    'wgs': 'EPSG:4326',
    'sk': 'EPSG:4284',
    # Other projections in loops below
}

# Add zones to proj
# Gauss
for i in range(20):
    PROJECTIONS[f'z{i}'] = f'EPSG:{28400 + i}'

# UTM
for i in range(20, 50):
    PROJECTIONS[f'{i}n'] = f'EPSG:{32600 + i}'

transformer = Transformer.from_crs(
    PROJECTIONS[args.in_proj], PROJECTIONS[args.out_proj])


def main():
    # Get content from clipboard
    content = pyperclip.paste()
    content = re.sub(r'° *|\' *', ' ', content)
    content = re.sub(r'"', '', content)

    # split rows, cells and convert to float
    data = [i.split("\t") for i in content.split("\n")]

    if re.search(r'\d{1,2} \d{1,2} \d{1,2}', data[0][0]):
        data = [[deg2dec(j) for j in i] for i in data if len(i) == 2]

    data = [[float(j) for j in i] for i in data if len(i) == 2]

    # Convert
    result = [list(transformer.transform(i[0], i[1])) for i in data]
    if out_deg:
        result = [[dec2deg(j) for j in i] for i in result]

    # Convert to string
    result_str = ''
    for row in result:
        result_str += "\t".join([str(i) for i in row]) + "\n"

    # Print to console
    for i, value in enumerate(data):
        print("\t".join([str(j) for j in value]),
              "\t".join([str(j) for j in result[i]]))

    pyperclip.copy(result_str)
    print('Copied to clipboard')


# -------------------MAIN----------------------#
if __name__ == '__main__':
    run(main)
