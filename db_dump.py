#!/usr/bin/env python
'''
dump "./data.xlsx" to postgresql "temp" database
'''

import os
import time
import pandas as pd
import numpy  as np
from sqlalchemy import create_engine


input_file = 'data.xlsx'

def main():

	# Connection params 
	input_file = os.path.join(os.environ['USERPROFILE'], 'Desktop', input_file)
	user = os.environ['POSTGRES_USER']
	password = os.environ['PGPASSWORD']
	db = 'temp'
	table = 'temp'

	# dump
	df = pd.read_excel(input_file)
	engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{db}')
	df.to_sql(table, engine, if_exists='replace')
	input(f'Done in {time.perf_counter()} sec')


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

