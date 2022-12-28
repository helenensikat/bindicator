#!/usr/bin/python

# The script checks if today is bin day for each of three bins and sets LEDs on if so (via cron job at 16:00 WST)
# Another script (bindicatoroff.py) will run via a cron job at 23:59 WST each day and set all the LEDs to off

# VARIABLES
# todaysdate = a YYYY-MM-DD string of the current date
# weekday = the day of the week when bindicator.py runs
# bindicatordata = data from the google sheet with bin days in it
# bindf = the data from bindicatordata in a dataframe
# redbinstatus, yellowbinstatus, greenbinstatus = whether it is bin day for each bin
# logger, file_handler, formatter = standard bits for logging

import RPi.GPIO as GPIO
import time
import logging
import pandas as pd
import gspread
import datetime
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials
gc = gspread.service_account(filename='bindicatorservicekey.json')

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

logger.info('bindcator.py initiated - all hail bindicator.py')

# Access bindicator sheet on google

gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1w2VzPjnQ2k-FKyZGZmNUijXnHCxcwxZbzztjAkefI1U/edit#gid=0")

# Get bindicator data from google sheet and test by printing google sheet content

bindicatordata = gsheet.sheet1.get_all_records()
print(bindicatordata) # Not necessary for bindication

# Convert  bindicator data from the google sheet to a dataframe

bindf= pd.DataFrame(bindicatordata)
print(bindf)

# Grab today's date in a pandas-friendly fashion
## For testing, comment out the first line and replace with:
## todaysdate = pd.Timestamp('2021-06-15').strftime('%Y-%m-%d')

todaysdate = pd.Timestamp.today().strftime('%Y-%m-%d') # Pandas is picky with date formatting - this returns it in a useable form
print('The date today is:')
print(todaysdate)

# Tell us what day of the week it is - not necessary for bindication

print('Today is a:')
weekday = bindf.at[bindf.loc[bindf['date'] == todaysdate].index[0],'weekday']
print(weekday)

# Now check today's bin statuses and print them

redbinstatus = bindf.at[bindf.loc[bindf['date'] == todaysdate].index[0],'redbin'] # Looks up the position of today's date in the 'date' column and finds the value in the equivalent row  of the 'redbin' column
yellowbinstatus = bindf.at[bindf.loc[bindf['date'] == todaysdate].index[0],'yellowbin']
greenbinstatus = bindf.at[bindf.loc[bindf['date'] == todaysdate].index[0],'greenbin']
print('Is it red bin night?')
print(redbinstatus)
print('Is it yellow bin night?')
print(yellowbinstatus)
print('Is it green bin night?')
print(greenbinstatus)

# Logging what happened above

logger.info('Date was ' + str(todaysdate) + '; day was ' + str(weekday) + '; redbin=' + str(redbinstatus) + '; yellowbin=' + str(yellowbinstatus) + ' greenbin=' + str(greenbinstatus) + '.')

# Let's set the lights and button up - code gets the lights and button connected to each pin ready to do stuff

button = 25
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Is this actually needed?
GPIO.setup(14,GPIO.OUT) # Red LED
GPIO.setup(15,GPIO.OUT) # Yellow LED
GPIO.setup(18,GPIO.OUT) # Green LED
GPIO.setup(23,GPIO.OUT) # LED on button
# COMMENT OUT FOR TESTING GPIO.setup(25,GPIO.IN,pull_up_down=GPIO.PUD_UP) # Button switch

# Lights testing sequence -  not necessary for bindication

GPIO.output(14,GPIO.HIGH) # Turns the light connected to pin 14 on
time.sleep(0.5) # Waits for a half-second
GPIO.output(14,GPIO.LOW) # Turns the light connected to pin 14 off
time.sleep(0.5)
GPIO.output(15,GPIO.HIGH)
time.sleep(0.5)
GPIO.output(15,GPIO.LOW)
time.sleep(0.5)
GPIO.output(18,GPIO.HIGH)
time.sleep(0.5)
GPIO.output(18,GPIO.LOW)
time.sleep(0.5)
GPIO.output(23,GPIO.HIGH)
time.sleep(0.5)
GPIO.output(23,GPIO.LOW)
time.sleep(0.5)

# Set lights on/off based on bin statuses

if redbinstatus == 'TRUE':
 GPIO.output(14,GPIO.HIGH)
 print('Put the red bin out.')
else:
 print('Keep the red bin in.')

if yellowbinstatus == 'TRUE':
 GPIO.output(15,GPIO.HIGH)
 print('Put the yellow bin out.')
else:
 print('Keep the yellow bin in.')

if greenbinstatus == 'TRUE':
 GPIO.output(18,GPIO.HIGH)
 GPIO.output(23,GPIO.HIGH) # No need to do the button separately because green bin always goes out and the button always lights up.
 print('Put the green bin out.')
else:
 print('Keep the green bin in.')

# GPIO.wait_for_edge(25,GPIO.FALLING,timeout=5000) # Add something here to close this out if nothing turned off by midnight.
# GPIO.output(14,GPIO.LOW)
# GPIO.output(15,GPIO.LOW)
# GPIO.output(18,GPIO.LOW)
# GPIO.output(23,GPIO.LOW)
# print('Bins out, lights off!')
