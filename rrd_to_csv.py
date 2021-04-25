import os
import glob
import csv
import rrdtool
from datetime import datetime
from pathlib import Path

basepath = os.getcwd()
basedir = os.listdir()
rrd_directories = []

# TODO  : CHANGE THIS AS YOU WISH / Smokeping Setting
csv_dir = 'csv_result'
consolidation_function = ['MIN', 'MAX', 'AVERAGE'] 
resolution = ['5m']
start_time = "2021-04-20"
end_time   = "2021-04-23"

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

def r_to_second(r):
	r_sec = 0
	if (r[-1] == 's'):
		r_sec = int(r[:-1]) 
	elif (r[-1] == 'm'):
		r_sec = int(r[:-1]) * 60
	elif (r[-1] == 'h'):
		r_sec = int(r[:-1]) * 3600
	return r_sec
	

def str_to_datetime(date):
	return int(datetime.strptime(date, '%Y-%m-%d').timestamp())

# Fetch data from RRD 
def fetch_rrd(rrd_file, cf, resolution, start, end):
	r = r_to_second(resolution)

	for t in range(start, end, r):
		data = rrdtool.fetch(f"{rrd_file}", f"{cf}", "-a" , "-r",  f"{resolution}", "-s", f"{t}", "-e", f"{end}")
		if (data[0][2] == r):
			return rrdtool.fetch(f"{rrd_file}", f"{cf}", "-a" , "-r",  f"{resolution}", "-s", f"{t}", "-e", f"{end}")
	return []


	
	



def format_rows(data):
	# consist of timestamped rows data {'timestamp': [value_1, value_2, etc]}
	rows = {}
	# database from RRA, without timestamp
	rra	 = data[2]
	# First timestamp for first row and will be increase as interval
	timestamp 		= data[0][0] + data[0][2]
	
	# Arrange row data to dictionary based on timestamp
	for row in rra:
		interval 		= data[0][2]
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
		base_name = os.path.basename(file).split('.')[0]

		for cf in consolidation_function:
			for r in resolution:
				# Fetching data from RRD. This should be based on smokeping setting Database		
				data 	= fetch_rrd(file, cf, r, str_to_datetime(start_time), str_to_datetime(end_time))
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





