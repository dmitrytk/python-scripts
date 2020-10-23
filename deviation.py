import sys
import os
import time
import re
from runner import run


DEVIATION_FOLDER = 'dev'
OUTPUT_FILE = 'result.txt'
OUTPUT_FILE2 = 'dev.txt'


def main():

    res = ''
    res_dev = 'WELL\tMD\tX\tY\tZ\tTVD\tDX\tDY\tAZIM\tINCL\tDLS\n'
    files = os.listdir(DEVIATION_FOLDER)
    st = '# WELL HEAD X-COORDINATE: 50329.7100'
    result = re.split(' +', st)
    for file in files:
        with open(f'{DEVIATION_FOLDER}/{file}') as f:
            content = f.read()
            content = content.split('\n')
            name = re.split(' +', content[1])[3]
            x = re.split(' +', content[2])[4]
            y = re.split(' +', content[3])[4]
            kb = re.split(' +', content[4])[3]
            mag = re.split(' +', content[5])[2]
            well = f'{name}\t{x}\t{y}\t{kb}\t{mag}\n'
            res += well
            for row in content[9:]:
                res_dev += name + '\t' + row + '\n'

    with open(OUTPUT_FILE, 'w') as f:
        f.write(res)
    with open(OUTPUT_FILE2, 'w') as f:
        f.write(res_dev)


# -------------------MAIN----------------------#
if __name__ == '__main__':
    run(main)
