#!/usr/bin/env python
"""
Fill blank row in layers table
Mandatory columns: Н_скв, ZK, ZP, COLL
Fill blank cell will be set to - 0
Input file format '%USERPROFILE%\\Desktop\\out.csv':
Н_скв	ZK	ZP	ZKA	ZPA	COLL	ZONE	APS	KP	KPR
100	1200	1200.2	1120.2	1120.4	0	-9999.99	0	0	0
100	1200.2	1245.9	1120.4	1166.1	0	-9999.99	0	0	0
100	1245.9	1248.8	1166.1	1169	1	Покурская верхняя	0.639	24.515	12.408
"""

import os
import time
import openpyxl as op
import pandas as pd
import re


def main():
    input_file = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'out.csv')
    output_file = os.path.join(
        os.environ['USERPROFILE'], 'Desktop', 'result.xlsx')

    # Update input file
    with open(input_file, 'r') as file:
        content = file.read()
        content = re.sub(';( {1,})?', ',', content)
    with open(input_file, 'w') as file:
        file.write(content)

    df = pd.read_csv(input_file, encoding='ansi')

    wb = op.Workbook()
    ws = wb.active

    # Columns in file
    base_columns = ['Н_скв', 'ZK', 'ZP']
    collector = 'COLL'
    params = [i for i in df.columns if i not in base_columns and i != collector]

    cols, rows = df.shape

    # Add header
    row = ['Н_скв', 'ZK', 'ZP']
    [row.append(i) for i in params]
    row.append('COLL')

    ws.append(row)

    for index, value in df.iterrows():
        if index < cols - 1:
            if df.ZP[index] != df.ZK[index + 1] and df['Н_скв'][index] == df['Н_скв'][index + 1]:
                row = [df['Н_скв'][index], df.ZK[index], df.ZP[index]]
                [row.append(df[i][index]) for i in params]
                row.append(df['COLL'][index])
                ws.append(row)

                row = [df['Н_скв'][index], df.ZP[index], df.ZK[index + 1]]
                [row.append(0) for i in params]
                row.append(0)
                ws.append(row)
            else:
                row = [df['Н_скв'][index], df.ZK[index], df.ZP[index]]
                [row.append(df[i][index]) for i in params]
                row.append(df['COLL'][index])
                ws.append(row)

        else:
            row = [df['Н_скв'][index], df.ZK[index], df.ZP[index]]
            [row.append(df[i][index]) for i in params]
            row.append(df['COLL'][index])
            ws.append(row)

    wb.save()
    os.system(f'start ""  {output_file}')


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
