'''
dump "data.xlsx" to postgresql
'''

import os
import time
import pandas as pd
import numpy  as np
from sqlalchemy import create_engine


file_name = 'data.xlsx'

def main():

	input_file = os.path.join('c:\\Users\\Dmitry\\Desktop', file_name)
	postgres_user = os.environ['POSTGRES_USER']
	postgres_password = os.environ['POSTGRES_PASSWORD']
	db_name = 'temp'
	table_name = 'temp'

	# dump
	df = pd.read_excel(input_file)
	engine = create_engine(f'postgresql://{postgres_user}:{postgres_password}@localhost:5432/{db_name}')
	df.to_sql(table_name, engine, if_exists='replace')
	input(f'Done in {time.perf_counter()} sec')


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		input(e)

