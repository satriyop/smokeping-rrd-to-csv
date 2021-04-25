import os
import glob
import csv
import rrdtool
from datetime import datetime
from pathlib import Path

basepath = os.getcwd()
basedir = os.listdir()
# TODO : Change this as you wish
csv_dir = 'csv_result'
rrd_directories = []

# Filter all directories and store in rrd_directories
# All rrd files should inside the base directory
for filename in os.listdir(basepath):
	f = os.path.join(basepath, filename)
	if os.path.isdir(f):
		rrd_directories.append(f)

# update created csv file with data fetched from rrd file
def write_to_csv(filename, header, rows):
	with open(filename, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(header)

		for timestamp, row_data in rows.items():
			row = [timestamp] + row_data
			writer.writerow(row)

# Fetch data from RRD 
def fetch_rrd(rrd_file, cf, resolution, start):
	data = rrdtool.fetch(f"{rrd_file}", f"{cf}", "-a" , "-r",  f"{resolution}", "-s", f"{start}")
	return data

def format_rows(data):
	# consist of timestamped rows data
	rows = {}
	# database from RRA, without timestamp
	rra	 = data[2]
	# First timestamp for first row and will be increase as interval
	timestamp 		= data[0][0] + data[0][2]
	interval 		= data[0][2]
	# Arrange row data to dictionary based on timestamp
	for row in rra:
		unix_timestamp 	= timestamp + interval
		human_timestamp = str(datetime.fromtimestamp(timestamp))
		row_data 		= list(row)

		rows.update({human_timestamp: row_data})
		
		timestamp = unix_timestamp

	return rows

def get_header(data):
	# add timestamp to existing header list, this will add new column later on
	return ['timestamp'] + list(data[1]) 

def create_csv_dir(dir_name):
	if not os.path.exists(dir_name):
		os.makedirs(os.path.join(basepath, dir_name))

def create_csv(base_name, cf, resolution, start_time):
	Path("{fn}-{cf}-{r}-{s}.csv".format(fn = base_name ,cf=cf, r=resolution, s=start_time)).touch(exist_ok=True)
	return "{fn}-{cf}-{r}-{s}.csv".format(fn = base_name, cf=cf, r=resolution, s=start_time)


# Prepare  directory as container for all csv files converted from rrd files
create_csv_dir(csv_dir)

# Filter files in rrd_directories to process only .rrd files
for dir in rrd_directories:
	files = Path(dir).glob("*rrd")	

	for file in files:
		# TODO  : CHANGE THIS AS YOU WISH
		#change this start time per your data starting time
		start_time = '20210401'

		consolidation_function = ['MIN', 'MAX', 'AVERAGE'] 

		# TODO : Change the resolution time as needed
		resolution = ['5m', '1h', '12h']
		base_name = os.path.basename(file).split('.')[0]

		for cf in consolidation_function:
			for r in resolution:
				# Fetching data from RRD. This should be based on smokeping setting Database		
				data 	= fetch_rrd(file, cf, r, start_time)
				# Formating data
				rows 	= format_rows(data)
				# Getting header row
				header 	= get_header(data)
				# Change dir to csv result directory
				os.chdir(os.path.join(basepath, csv_dir))
				# Create file based on CF and start time and resolution
				csv_file = create_csv(base_name,cf, r, start_time) 	
				# Write data to file
				write_to_csv(csv_file, header, rows)





