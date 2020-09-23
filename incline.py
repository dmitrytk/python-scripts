#!/usr/bin/env python
'''
Create .inc
Excel file template:
WELL    MD  INCL    AZIM
551 10  0.15    0
551 20  0.15    0
551 30  0.27    0
'''

import os
import glob
import time
import pandas as pd


INPUT_FILE = "incline.xlsx"
OUTPUT_DIR = 'inc'


def list_to_txt(output_file, content):
    '''Write 2d list to text file'''
    result_str = ''
    for row in content:
        result_str += '\t'.join([str(i) for i in row]) + '\n'
    with open(output_file, 'w') as f:
        f.write(result_str)


def main():
    df = pd.read_excel(INPUT_FILE)
    wells = set(df.WELL)

    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    for well in wells:
        well_df = df[df.WELL == well]
        result_list = [list(well_df)] + well_df.values.tolist()
        list_to_txt(f"./{OUTPUT_DIR}/{str(well)}.inc", result_list)


# -------------------MAIN----------------------#
if __name__ == "__main__":
    try:
        print("processing")
        main()
        print("Done!")
        time.sleep(3)
    except Exception as e:
        print(e)
        input()
