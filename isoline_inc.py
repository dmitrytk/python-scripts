#!/usr/bin/env python
"""
Create .inc files for Isoline
Excel file template:
Sheet <INCL>
WELL	MD	INC	AZIM
1026	20	0.75	0
1026	30	1.25	45

Sheet <HEADS>
WELL	X	Y	ALT	MAG
1026	12349908.45	6826920.269	62.42	19
6493	12348985.78	6826006.896	57.87	19
"""

import os
import pandas as pd
import time
from runner import run


INPUT_FILE = 'incline.xlsx'
OUTPUT_DIR = 'inc'
INCL_SHEET_NAME = 'INCL'
HEADS_SHEET_NAME = 'HEADS'


def main():
    df_incl = pd.read_excel(INPUT_FILE, sheet_name=INCL_SHEET_NAME)
    df_heads = pd.read_excel(INPUT_FILE, sheet_name=HEADS_SHEET_NAME)

    wells = list(set(df_incl.WELL))

    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    for well in wells:
        df_well_incl = df_incl[df_incl.WELL == well]
        df_well_heads = df_heads[df_heads.WELL == well]
        if df_well_heads.empty:
            continue
        result_str = f'WELL NAME:\t{well}\n'
        result_str += f'X:\t{df_well_heads.X.iloc[0]}\n'
        result_str += f'Y:\t{df_well_heads.Y.iloc[0]}\n'
        result_str += f'ALT:\t{df_well_heads.ALT.iloc[0]}\n'
        result_str += f'MAG:\t{df_well_heads.MAG.iloc[0]}\n'
        result_str += 'MD\tINC\tAZIM\n'

        for _, row in df_well_incl.iterrows():
            result_str += f'{row.MD}\t{row.INC}\t{row.AZIM}\n'

        with open(f'{OUTPUT_DIR}/{well}.inc', 'w') as f:
            f.write(result_str)


# -------------------MAIN----------------------#
if __name__ == '__main__':
    run(main)
