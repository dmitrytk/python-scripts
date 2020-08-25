#!/usr/bin/env python
"""
Calculate average parameters for zones and wells from Geopoisk layers table
!!!<COLL> column is required!!!
Input csv file  "%USERPROFILE%\\Desktop\\out.csv":
Н_скв	ZK	ZP	ZKA	ZPA	COLL	ZONE	APS	KP	KPR
100	1200	1200.2	1120.2	1120.4	0	-9999.99	0	0	0
100	1200.2	1245.9	1120.4	1166.1	0	-9999.99	0	0	0
100	1245.9	1248.8	1166.1	1169	1	Покурская верхняя	0.639	24.515	12.408
Output excel file '%USERPROFILE%\\Desktop\\result.xlsx'
"""

import pandas as pd
import re
import time
import sys
import openpyxl as op
import sqlite3
import os


def main():
    input_file = os.path.join(os.environ['USERPROFILE'], 'Desktop','out.csv')
    output_file = os.path.join(os.environ['USERPROFILE'], 'Desktop','result.xlsx')

    # Update input file
    with open(input_file, 'r') as file:
        content = file.read()
        content = re.sub(";( {1,})?", ",", content)
    with open(input_file, 'w') as file:
        file.write(content)


    default_columns = [
        "WELL", "ZK", "ZP", "ZKA", "ZPA", "COLL", "NOB", "H", "ZONE",
        "HORIZONT"
    ]

    zone_name = "Объект"

    # Load file
    df = pd.read_csv(input_file, encoding='ansi')
    df = df.rename(columns={'Н_скв': 'WELL'})
    df = df[df.COLL > 0]
    df = df[df.ZONE != "-9999.99"]
    if "H" not in df.columns.values:
        df["H"] = df["ZPA"] - df["ZKA"]

    df['HORIZONT'] = zone_name

    # Load data to sqlite
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    df.to_sql("data", con=conn, if_exists='replace')

    params = []
    [params.append(i) for i in list(df) if i not in default_columns]

    #   Create 1 SQL query
    QUERY = "SELECT COLL, WELL, ZONE, round(sum(H),2) as H, "
    for param in params:
        QUERY += "round(sum(" + param + "*H)/sum(H),2) as " + param + ", "
    QUERY = QUERY[:-2]
    QUERY += " FROM data group by COLL, ZONE, WELL;"

    df1 = pd.read_sql_query(QUERY, conn)

    # Store query values in list
    result_list = df.values.tolist()

    # Create 2 SQL query
    QUERY_2 = "SELECT COLL, WELL, HORIZONT, round(sum(H),2) as H, "
    for param in params:
        QUERY_2 += "round(sum(" + param + "*H)/sum(H),2) as " + param + ", "
    QUERY_2 = QUERY_2[:-2]
    QUERY_2 += " FROM data group by COLL, WELL;"

    df2 = pd.read_sql_query(QUERY_2, conn)

    cursor.close()
    conn.close()

    # Concatenate result dataframes and save to excel
    df_result = pd.concat([df1, df2])
    df_result.to_excel(output_file)

    os.system(f'start ""  {output_file}')


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
