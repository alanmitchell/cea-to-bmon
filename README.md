# cea-to-bmon

Script to post data from Chugach Electric Meter files to BMON servers.
Different meters can post data to different BMON servers.  This script
is generally run from a CRON job, processing any new meter files.

Usage is:

    process_meters.py <config file path>

    as an example:

    ./process_meters.py /home/cea/cea_config/config.yaml

The configuration file is required and controls operation of the script.
The `config_example.yaml` file is a sample configuration file.  When the script
runs, it places logging information in the a subdirectory of the configuration
files named `logs`.  It also places some miscellaneous files needed for operation
in a subdirectory named `run`.  These two directories *must* be created prior to
running the script.

Each section of the configuration file is described below.  The file is in YAML format.

    meter_files: /home/cea/meters/*.csv

The `meter_files` value is a Python
[glob pattern](https://docs.python.org/2/library/glob.html) that identifies the meter files to process.  All of the files matching the glob pattern will be
processed by the script.  Here is an excerpt from a valid meter file:

    L131776533,2017-12-29 00:00:00,.0918,,245.6178,,
    L131776533,2017-12-29 00:15:00,.1194,,245.7600,,
    L131776533,2017-12-29 00:30:00,.1170,,245.2622,,
    L131776533,2017-12-29 00:45:00,.1020,,243.9111,,

Each meter file is a CSV file with no header row.  The rows give electricity
consumption data for 15 minute intervals.  Each row has at least 3 fields and
the first three fields contain the following information:

    Field 1:  The Meter Number
    Field 2:  A date/time string of the format shown in the above sample
    Field 3:  The number of kWh that occur in the 15 minute interval starting
              at the above time stamp.
.

    delete_after_process: True

If `delete_after_process` is True, then each meter file will be deleted after it
is processed.  However, if any errors occur while processing the file, the file
will not be deleted.

    meter_number_db: /home/cea/meter_db/meters.sqlite

`meter_number_db` is the full path to a SQLite database file that has a
`meters` table.  The `meters` table must have two text fields: `meter_number` and
`bmon_id`.  Each row of the table specifies the BMON server that should be posted
to for the specified meter number.  BMON servers are named with short text names
such as "ahfc".  Information for each BMON server is given later in the
configuration file.

A tool such as [phpLiteAdmin](https://www.phpliteadmin.org/) can be configured to
allow an Admin user to edit the list of meter numbers and associated BMON servers.

    logging_level: INFO

`logging_level` is one of the standard logging levels for Python's logging
module; this controls the detail of information shown in the script's logging
file.

    time_zone: US/Alaska

`time_zone` is a timezone from the [tz database](https://en.wikipedia.org/wiki/Tz_database).  The timestamps in the meter files are assumed
to be in this timezone.

    bmon_servers:
      ahfc:
        url: https://bms.ahfc.us/readingdb/reading/store/
        store_key: xyz
      an:
        url: https://bmon.analysisnorth.com/readingdb/reading/store/
        store_key: def

In the `bmon_servers` section of the configuration file, additional information
is given for each of the BMON server abbreviations that appear in the
`meter_number_db` database discusssed above.  The URL and store key of the
BMON server must be specified for each BMON server, as shown in the sample above.
