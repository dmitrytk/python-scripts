"""
Calculate average parameters for zones and wells from Geopoisk layers table
!!!<COLL> column in necessary!!!
Input csv file  "D:\\Takkand_D\\Desktop\\out.csv":
Н_скв	ZK	ZP	ZKA	ZPA	COLL	ZONE	APS	KP	KPR
100	1200	1200.2	1120.2	1120.4	0	-9999.99	0	0	0
100	1200.2	1245.9	1120.4	1166.1	0	-9999.99	0	0	0
100	1245.9	1248.8	1166.1	1169	1	Покурская верхняя	0.639	24.515	12.408
Output excel file 'D:\\Takkand_D\\Desktop\\result.xlsx'
"""

import pandas as pd
import time
import sys
import openpyxl as op
import sqlite3
import os

os.system("cls")


def main():
    print('processing')
    default = [
        "WELL", "ZK", "ZP", "ZKA", "ZPA", "COLL", "NOB", "H", "ZONE",
        "HORIZONT"
    ]
    zone_name = "Объект"

    df = pd.read_csv("D:\\Takkand_D\\Desktop\\out.csv", encoding='ansi')
    df = df.rename(columns={'Н_скв': 'WELL'})
    df = df[df.COLL > 0]
    df = df[df.ZONE != "-9999.99"]
    if "H" not in df.columns.values:
        df["H"] = df["ZPA"] - df["ZKA"]

    df['HORIZONT'] = zone_name

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    df.to_sql("data", con=conn, if_exists='replace')

    params = []
    [params.append(i) for i in list(df) if i not in default]

    #------------------CREATE  SQL QUERY------------------#
    QUERY = "SELECT COLL, WELL, ZONE, round(sum(H),2) as H, "
    for param in params:
        QUERY += "round(sum(" + param + "*H)/sum(H),2) as " + param + ", "
    QUERY = QUERY[:-2]
    QUERY += " FROM data group by COLL, ZONE, WELL;"

    result_list = []
    df = pd.read_sql_query(QUERY, conn)
    result_list.append(list(df))
    temp = df.apply(lambda x: x.tolist(), axis=1)

    QUERY_2 = "SELECT COLL, WELL, HORIZONT, round(sum(H),2) as H, "
    for param in params:
        QUERY_2 += "round(sum(" + param + "*H)/sum(H),2) as " + param + ", "
    QUERY_2 = QUERY_2[:-2]
    QUERY_2 += " FROM data group by COLL, WELL;"

    df = pd.read_sql_query(QUERY_2, conn)

    cursor.close()
    conn.close()

    temp_2 = df.apply(lambda x: x.tolist(), axis=1)

    [result_list.append(i) for i in temp]
    [result_list.append(i) for i in temp_2]

    wb = op.Workbook()
    ws = wb.active
    [ws.append(i) for i in result_list]

    wb.save("D:\\Takkand_D\\Desktop\\result.xlsx")
    os.system('start ""  D:\\Takkand_D\\Desktop\\result.xlsx"')
    print(f"Done in {time.perf_counter()} sec")


# -------------------------------------------------#
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        input()