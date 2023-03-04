# About bindicator

Electronics project with light-up mini-bins to show which rubbish bins to put on the kerb each week.

# Setting up bindicator to run daily

This can be configured to run as a service, triggered by a cron job that checks whether it is bin night daily, and turns the lights off at midnight if they have not already been turned off manually using a button.

The following assumes the path for bindicator.py is /usr/scripts/bindicator/bindicator.py and the path for bindicatoroff.py is /usr/scripts/bindicator/bindicatoroff.py

In this case the user is 'bindicator', created for working on this project.  If you create a new user, remember to add them to the GPIO group:

sudo adduser pi gpio

Create the service here: /lib/systemd/system/bindicator.service

Content for bindicator.service:

[Unit]
Description=Bindicator Service
After=multi-target.target

[Service]
Type=simple
ExecStart=/usr/scripts/bindicator/bindicator.py

[Install]
WantedBy=multi-target.target

Set permissions:
sudo chmod 644 /lib/systemd/system/bindicator.service

Set up the cron jobs by adding the following to crontab (these run the service to check at 4pm whether it is bin night, light up the appropriate LEDs and the button LED if so, and turn off any lights that are still on at midnight):

58 15 * * * sudo systemctl stop bindicator.service

59 15 * * * sudo systemctl daemon-reload

00 16 * * * sudo systemctl start bindicator.service

58 23 * * * sudo systemctl stop bindicator.service

59 23 * * * cd /usr/scripts/bindicator/ && /usr/bin/python /usr/scripts/bindicator/bindicatoroff.py

Lastly, the systemctl cron jobs won't run without a sudo password, but this can be resolved as follows (assuming they are being run by user 'pi' when the cron jobs trigger:

Run 'sudo visudo' then add this line to the file: 
pi ALL=NOPASSWD:/usr/bin/systemctl start bindicator.service,/usr/bin/systemctl stop bindicator.service,usr/bin/systemctl daemon-reload


