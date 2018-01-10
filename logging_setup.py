"""Configures Logging for an application.
"""

import logging
import logging.handlers

def configure_logging(log_file):
    # Use the root logger for the application.

    # stop propagation of messages from the 'requests' module
    logging.getLogger('requests').propagate = False

    # create a rotating file handler
    fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=200000, backupCount=5)

    # create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    fh.setFormatter(formatter)

    # create a handler that will print to console as well.
    console_h = logging.StreamHandler()
    console_h.setFormatter(formatter)

    # add the handlers to the logger
    logging.root.addHandler(fh)
    logging.root.addHandler(console_h)

