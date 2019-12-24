"""
Load xlsx data to sqlite db
Format of data.xlsx file:
WELL	DATE	RATE
SVA-1063	01.03.2018 5:00	1258.560059
SVA-1063	02.03.2018 5:00	1245.600098
SVA-1063	03.03.2018 5:00	1251.360107

input file: data.xlsx
output file: data.slite
"""
import pandas as pd
import time
import sqlite3

input_file = 'data.xlsx'
output_file = 'data.sqlite'

def main():
	print('processing')
	df = pd.read_excel(input_file)
	conn = sqlite3.connect(output_file)
	cursor = conn.cursor()
	df.to_sql("data", con=conn, if_exists='replace')

	input(f'Done in {time.perf_counter()} sec')

if __name__=='__main__':
	try:
		main()
	except Exception as e:
		print(e)
		input('Press Enter to exit.')
	