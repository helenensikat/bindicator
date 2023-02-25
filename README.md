About bindicator

Electronics project with light-up mini-bins to show which rubbish bins to put on the kerb each week.

This can be configured to run as a service, triggered by a cron job that checks whether it is bin night daily, and turns the lights off at midnight if they have not already been turned off manually using a button.

The following assumes the path for bindicator.py is /usr/scripts/bindicator/bindicator.py and the path for bindicatoroff.py is /usr/scripts/bindicator/bindicatoroff.py

Create the service here: /lib/systemd/system/bindicator.service

Content for bindicator.service:

[Unit]
Description=Bindicator Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/scripts/bindicator/ && /usr/bin/python /usr/scripts/bindicator/bindicator.py  >> /usr/scripts/bindicator/crontestbindicator.txt  2>&1
User=root

[Install]
WantedBy=multi-user.target

Set permissions:
sudo chmod 644 /lib/systemd/system/bindicator.service

Set up the cron jobs by adding the following to crontab (these run the service to check whether it is bin night, light up the appropriate LEDs and the button LED if so, and turn off any lights that are still on at midnight):

00 16 * * * systemctl start bindicator.service
58 23 * * * systemctl stop bindicator.service
59 23 * * * cd /usr/scripts/bindicator/ && /usr/bin/python /usr/scripts/bindicator/bindicatoroff.py