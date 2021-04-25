# smokeping-rrd-to-csv
convert rrd files in smokeping to csv files based on consolidation function

## Find your smokeping setting for database
/etc/smokeping/config.d/Database

## Adjust the start time and resolution time in the code as your smokeping setting
You may want to see the diagram to know what are the resolution time available for your system

## Running the script
	python rrd_to_csv.py
  
# Result 
Csv files that are generated will be in csv_result directory. You may want to change this in the code as you wish
