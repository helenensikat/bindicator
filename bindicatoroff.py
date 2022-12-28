#!/usr/bin/python

# Cron job runs every day at 11:59 WST to turn all the lights off. 

import RPi.GPIO as GPIO
import logging

# Get or create a logger

logger = logging.getLogger(__name__)

# Set log level

logger.setLevel(logging.INFO)

# Define file handler and set formatter for logging

file_handler = logging.FileHandler('bindicator.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# Add file handler to logger

logger.addHandler(file_handler)

# Logs

logger.info('bindcatoroff.py ran - goodnight!')

# Setting things up to do stuff with the lights on each pin

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Is there a need for this line?
GPIO.setup(14,GPIO.OUT) # Red LED
GPIO.setup(15,GPIO.OUT) # Yellow LED
GPIO.setup(18,GPIO.OUT) # Green LED
GPIO.setup(23,GPIO.OUT) # LED button

# Turn all the lights off

GPIO.output(14,GPIO.LOW)
GPIO.output(15,GPIO.LOW)
GPIO.output(18,GPIO.LOW)
GPIO.output(23,GPIO.LOW)
