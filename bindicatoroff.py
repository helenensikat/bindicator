#!/usr/bin/python

# CONTEXT

# Should be triggered via a cron job every day at 11:59 WST to turn all the lights off. 

# CODE

# Import libraries

from gpiozero import LED
import logging
import sys

# Define devices associated with pins

redled = LED(14)
yellowled = LED(15)
greenled = LED(18)
buttonled = LED(23)

# Set up logging

logger = logging.getLogger(__name__) # Get or create a logger
logger.setLevel(logging.INFO) # Set log level
file_handler = logging.FileHandler('bindicator.log') # 3 lines define file handler and set formatter for logging
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) # Add file handler to logger
logger.info('bindcatoroff.py ran - goodnight!') # Output to logger

# Turn all the lights off and exit script

redled.off()
yellowled.off()
greenled.off()
buttonled.off()
sys.exit()
