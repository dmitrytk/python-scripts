#!/usr/bin/env python
'''
Create separate .inc file for each well
Excel file template (case sensitive):
WELL    MD  INCL    AZIM
551 10  0.15    0
551 20  0.15    0
551 30  0.27    0
'''

import os
import glob
import time
import pandas as pd


input_file = "incline.xlsx"
output_dir = 'inc'


def list_to_txt(output_file, content):
    '''Write 2d list to text file'''
    result_str = ''
    for row in content:
        result_str += '\t'.join([str(i) for i in row]) + '\n'
    with open(output_file, 'w') as f:
        f.write(result_str)


def main():
    df = pd.read_excel(input_file)
    wells = set(df.WELL)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for well in wells:
        well_df = df[df.WELL == well]
        result_list = [list(well_df)] + well_df.values.tolist()
        list_to_txt(f"./{output_dir}/{str(well)}.inc", result_list)


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
