#!/usr/bin/env python
"""
Calculate average parameters for zones and wells from Geopoisk layers table
!!!<KOL> column is required!!!
Input csv file  '%USERPROFILE%\\Desktop\\out.csv':
Н_скв	ZK	ZP	ZKA	ZPA	KOL	ZONE	APS	KP	KPR
100	1200	1200.2	1120.2	1120.4	0	-9999.99	0	0	0
100	1200.2	1245.9	1120.4	1166.1	0	-9999.99	0	0	0
100	1245.9	1248.8	1166.1	1169	1	Покурская верхняя	0.639	24.515	12.408
Output excel file '%USERPROFILE%\\Desktop\\result.xlsx'
"""

import sys
import os
import time
import re
import pandas as pd
import openpyxl as op
import sqlite3


INPUT_FILE = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'out.csv')
OUTPUT_FILE = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'result.xlsx')


def main():
    # Update input file
    with open(INPUT_FILE, 'r') as file:
        content = file.read()
        content = re.sub(";( {1,})?", ",", content)
    with open(INPUT_FILE, 'w') as file:
        file.write(content)

    default_columns = [
        'WELL', 'ZK', 'ZP', 'ZKA', 'ZPA', 'KOL', 'NOB', 'H', 'ZONE',
        'HORIZONT'
    ]

    zone_name = 'Объект'

    # Load file
    df = pd.read_csv(INPUT_FILE, encoding='ansi')
    df = df.rename(columns={'Н_скв': 'WELL'})
    df = df[df.KOL == 'Коллектор']
    df = df[df.ZONE != '-9999.99']
    if 'H' not in df.columns.values:
        df['H'] = df['ZPA'] - df['ZKA']

    df['HORIZONT'] = zone_name

    # Load data to sqlite
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    df.to_sql('data', con=conn, if_exists='replace')

    params = [i for i in list(df) if i not in default_columns]

    # Create SQL query
    # Average params group by WELL and ZONES
    QUERY = 'SELECT \n\tWELL,\n\tZONE,\n\tround(sum(H),2) as H,\n'
    QUERY += ',\n'.join(
        [f'\tround(sum({param}*H)/sum(H),2) as {param}' for param in params])
    QUERY += '\nFROM data group by ZONE, WELL\n'

    QUERY += 'UNION\n'

    # Average params group by WELL
    QUERY += "SELECT \n\tWELL,\n\t'ВСЕ' as ZONE,\n\tround(sum(H),2) as H,\n"
    QUERY += ",\n".join(
        [f'\tround(sum({param}*H)/sum(H),2) as {param}' for param in params])
    QUERY += '\nFROM data group by WELL;'

    # Execute QUERY
    df_result = pd.read_sql_query(QUERY, conn)

    cursor.close()
    conn.close()

    # Save to excel
    df_result.to_excel(OUTPUT_FILE)

    os.system(f'start ""  {OUTPUT_FILE}')


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
