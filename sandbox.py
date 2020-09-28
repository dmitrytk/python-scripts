#!/usr/bin/env python
"""
Create .inc files for Isoline
Excel file template:
WELL	MD	X	Y	ALT	INC	AZIM	MAG
103	40	13629651	6836114	104.7	0.38	185	17.67
"""

import os
import pandas as pd
import time


INPUT_FILE = 'incline.xlsx'
OUTPUT_DIR = 'inc'


def main():
    df_incl = pd.read_excel(INPUT_FILE, sheet_name='incl')
    df_heads = pd.read_excel(INPUT_FILE, sheet_name='heads')

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
    try:
        print('processing')
        main()
        print('Done!')
        time.sleep(3)
    except Exception as e:
        print(e)
        input()
