#!/usr/local/bin/python2.7

import glob
import logging
import os
import csv
import sys
import time
import yaml

import logging_setup
from httpPoster2 import HttpPoster, BMSreadConverter

# configuration file name, 1st command line argument
config_fn = sys.argv[1]

# get path to folder where config file is.  This folder
# is used to store logs and other files.
config_folder = os.path.dirname(config_fn)

# ----- Setup Exception/Debug Logging for the Application

# Log file for the application.
log_file = os.path.join(config_folder, 'logs', 'process_meters.log')

logging_setup.configure_logging(log_file)

# -------------------

try:
    # load configuration file describing general operation of this script
    # and the files to be loaded.
    config = yaml.load(open(config_fn))

except:
    logging.exception('Error in Reading Configuration File.')
    sys.exit()

try:
    # set the log level. Because we are setting this on the logger, it will apply
    # to all handlers (unless maybe you set a specific level on a handler?).
    # defaults to INFO if a bad entry in the config file.
    logging.root.setLevel(getattr(logging, config['logging_level'].upper(), 20))

    # start BMON posters and put in a dictionary
    posters = {}
    for id, bmon_info in config['bmon_servers'].items():
        posters[id] = HttpPoster(bmon_info['url'],
                                 reading_converter=BMSreadConverter(bmon_info['store_key']),
                                 post_q_filename=os.path.join(config_folder, 'run', '%s_postQ.sqlite' % id),
                                 post_thread_count=1,
                                 post_time_file=os.path.join(config_folder, 'run', '%s_last_post_time' % id)
                                )
except:
    logging.exception('Error in Script Initialization.')
    sys.exit()

# Loop through files to process
for fn in glob.glob(config['meter_files']):

    # make dictionary keyed on meter number
    # to hold readings
    readings = {}
    
    with open(fn, 'rb') as csvfile:
        for row in csv.reader(csvfile):
            meter_num, ts_str, kwh = row[:3]
            kwh = float(kwh)
            # convert timestamp string to Unix Epoch time.

            rec = (ts, meter_num, kwh)

            # add to list of readings
            reading_list =  readings.get(meter_num, [])
            reading_list.append(rec)
            readings[meter_num] = reading_list

    # add readings to correct BMON poster
    for meter_num, reading_list in readings.items():
        poster_for_meter = posters[config['meter_to_bmon'][meter_num]]
        poster_for_meter.add_readings(reading_list)

    # delete meter file
    os.remove(fn)

# wait until BMON posters finish their work or stop 
# making progress.
last_remaining_count = 0
while True:
    remaining_count = 0
    for id, poster in posters.items():
        remaining_count += poster.items_remaining()

    if remaining_count == 0 or remaining_count == last_remaining_count:
        break
    last_remaining_count = remaining_count

    # wait a few seconds before checking again.  this needs to be long enough
    # so that posting progress can be made.
    time.sleep(10)
