#!/usr/bin/python

# CONTEXT

# The script checks if today is bin day for each of three bins and sets LEDs on if so.
# The script should be run as a service (bindicator.service) at 16:00 WST to allow off-button to remain working when not SSH'd in; setting full path for gc filename prevents error when service runs. 
# Another script (bindicatoroff.py) should be triggered via a cron job at 23:59 WST each day and set all the LEDs to off

# VARIABLES

# todaysdate = a YYYY-MM-DD string of the current date
# weekday = the day of the week when bindicator.py runs
# bindicatordata = data from the google sheet with bin days in it
# bindf = the data from bindicatordata in a dataframe
# redbinstatus, yellowbinstatus, greenbinstatus = whether it is bin day for each bin
# logger, file_handler, formatter = standard bits for logging

# CODE

# Import libraries

from gpiozero import Button
from gpiozero import LED
from signal import pause
from time import sleep
import pandas as pd
import gspread
import logging
from datetime import date
import sys
from oauth2client.service_account import ServiceAccountCredentials
gc = gspread.service_account(filename='/usr/scripts/bindicator/bindicatorservicekey.json')

# Define devices associated with pins

redled = LED(14)
yellowled = LED(15)
greenled = LED(18)
buttonled = LED(23)
binbutton = Button(25)

# Set up logging

logger = logging.getLogger(__name__) # Get or create a logger
logger.setLevel(logging.INFO) # Set log level
file_handler = logging.FileHandler('bindicator.log')  # 3 lines define file handler and set formatter for logging
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) # Add file handler to logger
logger.info('bindcator.py initiated - all hail bindicator.py') # Output to logger

# Get data from bindicator sheet on Google Drive

gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1w2VzPjnQ2k-FKyZGZmNUijXnHCxcwxZbzztjAkefI1U/edit#gid=0")
bindicatordata = gsheet.sheet1.get_all_records() # Get bindicator data from google sheet and test by printing google sheet content
print(bindicatordata) # Diagnostics
bindf= pd.DataFrame(bindicatordata) # Convert bindicator data from the google sheet to a dataframe
print(bindf) # Diagnostics

# Grab today's date in a pandas-friendly fashion and print it and the day of the week for diagnostics

todaysdate = pd.Timestamp.today().strftime('%Y-%m-%d') # Pandas is picky with date formatting - this returns it in a useable form
print('The date today is:')
print(todaysdate)
print('Today is a:')
weekday = bindf.at[bindf.loc[bindf['date'] == todaysdate].index[0],'weekday']
print(weekday)

# Check today's bin statuses and print them for diagnostics

redbinstatus = bindf.at[bindf.loc[bindf['date'] == todaysdate].index[0],'redbin'] # Looks up the position of today's date in the 'date' column and finds the value in the equivalent row  of the 'redbin' column
yellowbinstatus = bindf.at[bindf.loc[bindf['date'] == todaysdate].index[0],'yellowbin']
greenbinstatus = bindf.at[bindf.loc[bindf['date'] == todaysdate].index[0],'greenbin']
print('Is it red bin night?')
print(redbinstatus)
print('Is it yellow bin night?')
print(yellowbinstatus)
print('Is it green bin night?')
print(greenbinstatus)

# Log what happened when today's bin statuses were checked

logger.info('Date was ' + str(todaysdate) + '; day was ' + str(weekday) + '; redbin=' + str(redbinstatus) + '; yellowbin=' + str(yellowbinstatus) + ' greenbin=' + str(greenbinstatus) + '.')

# Lights testing sequence -  not necessary for bindication

redled.on() # Turns the LED on the red bin on
sleep(0.5) # Waits for a half-second
redled.off() # Turns the LED on the red bin off
sleep(0.5)
yellowled.on()
sleep(0.5)
yellowled.off()
sleep(0.5)
greenled.on()
sleep(0.5)
greenled.off()
sleep(0.5)
buttonled.on()
sleep(0.5)
buttonled.off()
sleep(0.5)

# Set lights on/off based on bin statuses, and print a message about what to do with each bin

if redbinstatus == 'TRUE':
 redled.on()
 print('Put the red bin out.')
else:
 print('Keep the red bin in.')

if yellowbinstatus == 'TRUE':
 yellowled.on()
 print('Put the yellow bin out.')
else:
 print('Keep the yellow bin in.')

if greenbinstatus == 'TRUE':
 greenled.on()
 buttonled.on() # No need to do the button separately because green bin always goes out and the button always lights up
 print('Put the green bin out.')
else:
 print('Keep the green bin in.')

# Exit script if no bins are going out tonight

if greenbinstatus == 'FALSE' and yellowbinstatus == 'FALSE' and greenbinstatus == 'FALSE':
    sys.exit()

# Detect when button is double-pressed, turn off all lights, and exit script

while True:
        binbutton.wait_for_press()
        binbutton.wait_for_release()
        if binbutton.wait_for_press(timeout=0.6):
                redled.off()
                yellowled.off()
                greenled.off()
                buttonled.off()
                print('Lights out.') # Diagnostics
                sys.exit()