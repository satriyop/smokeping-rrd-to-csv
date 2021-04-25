# smokeping-rrd-to-csv
convert rrd files in smokeping to csv files based on consolidation function

## Find your smokeping setting for database
	/etc/smokeping/config.d/Database

## Adjust the Consolidation Function(CF), Resolution (r), and Start time your smokeping setting
### TODO  : CHANGE THIS CODE AS YOU WISH / based on Smokeping Setting
	csv_dir = 'csv_result'
	consolidation_function = ['MIN', 'MAX', 'AVERAGE'] 
	resolution = ['5m', '1h', '12h']
	start_time = '20210401'

### To understand the RRD in smokeping
You may want to see the diagram to know what are the resolution time available for your system
	open smokeping_RRD.drawio

Optional :  You might want to examine the original data by dumping the RRD file to XML file via rrdtool command 
	rrdtool dump file.rrd > file.xml

## Running the script
- Make sure your rrd files are contained on a directory
- The script will execute all directory in the base directory and try to find .rrd files extension
- Example in this repo is directory FW, RTR, SWITCH as directories that contain .rrd file
- At the base directory run below command :

	python rrd_to_csv.py
  
# Result - CSV files generated 
Csv files that are generated will be in csv_result directory. You may want to change this in the code as you wish
	// Change this
	csv_dir = 'csv_result'
