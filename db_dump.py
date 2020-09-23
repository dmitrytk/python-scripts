#!/usr/bin/env python
"""
dump '%USERPROFILE%\\Desktop\\data.xlsx' to postgresql 'temp' database
"""

import os
import time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


INPUT_FILE = 'data.xlsx'
DB = 'temp'
TABLE = 'temp'


def main():
    # Connection params
    file = os.path.join(os.environ['USERPROFILE'], 'Desktop', INPUT_FILE)
    user = os.environ['PGUSER']
    password = os.environ['PGPASSWORD']

    # dump
    df = pd.read_excel(file)
    engine = create_engine(
        f'postgresql://{user}:{password}@localhost:5432/{DB}')
    df.to_sql(TABLE, engine, if_exists='replace')
    input(f'Done in {time.perf_counter()} sec')


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
