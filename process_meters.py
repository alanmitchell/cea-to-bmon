#!/usr/local/bin/python
# set up logging

# read configuration file

# start BMON posters and put in a dictionary

# Loop through files to process
for fn in glob.glob(cfg['meter_files']):

    # make dictionary keyed on meter number
    # to hold readings
    readings = {}
    
    readings = []
    for lin in open(fn):

        # parse line into fields
        # add to list of readings
        reading_list =  readings.get(meter_number, [])
        reading_list.append(this_reading)
        readings[meter_number] = reading_list

    # add readings to correct BMON poster

    # delete old meter files 

# wait until BMON posters finish their work or stop 
# making progress.
