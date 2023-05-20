# About bindicator

Electronics project with light-up mini-bins to show which rubbish bins to put on the kerb each week.

# Setting up bindicator to run daily

This can be configured to run as a service and a timer to check whether it is bin night each afteroon; currently being lazy and using a cron job to lights off at midnight if they have not already been turned off manually using a button.

The following assumes the path for bindicator.py is /usr/scripts/bindicator/bindicator.py and the path for bindicatoroff.py is /usr/scripts/bindicator/bindicatoroff.py

In this case the user is 'bindicator', created for working on this project; the 'bindicator' user and the 'pi' user have both been added to the group %bindicator.  If you create a new user, remember to add them to the GPIO group:

sudo adduser pi gpio

Create the service here: /lib/systemd/system/bindicator.service

Content for bindicator.service:

[Unit]
Description=Bindicator Service
After=multi-target.target

[Service]
Type=simple
ExecStart=sudo /usr/bin/python  /usr/scripts/bindicator/bindicator.py

[Install]
WantedBy=multi-target.target

Create the timer here: /lib/systemd/system/bindicator.timer

Content for bindicator.timer:

[Unit]
Description=Run bindicator script at 16:00 daily

[Timer]
##Run every at at 16:00
OnCalendar=*-*-* 16:00:00
#File describing job to execute
Unit=bindicator.service

[Install]
WantedBy=timers.target

Set permissions:
sudo chmod 644 /lib/systemd/system/bindicator.service
sudo chmod 644 /lib/systemd/system/bindicator.timer

Set up the cron jobs by adding the following to crontab (these do a bit of cleanup before the timer runs bindicator.service at 4pm to check whether it is bin night, and turns off any lights that are still on at midnight):

56 15 * * * sudo /usr/bin/systemctl daemon-reload
55 15 * * * sudo /usr/bin/systemctl enable bindicator.service
58 15 * * * sudo /usr/bin/systemctl enable bindicator.timer
59 15 * * * sudo /usr/bin/systemctl start bindicator.timer
59 23 * * * cd /usr/scripts/bindicator/ && /usr/bin/python /usr/scripts/bindicator/bindicatoroff.py

Lastly, the systemctl cron jobs won't run without a sudo password, but this can be resolved as follows (assuming they are being run by user in the group %bindicator when the cron jobs trigger:

Run 'sudo visudo' then add this line to the file: 
%bindicator ALL=NOPASSWD:/usr/bin/systemctl start bindicator.service, /usr/bin/systemctl stop bindicator.service, /usr/bin/systemctl daemon-reload,/usr/bin/systemctl enable bindicator.service, /usr/bin/python /usr/scripts/bindicator/bindicator.py, /usr/bin/systemctl enable bindicator.timer, /usr/bin/systemctl start bindicator.timer

The cron job, service, and sudoers setups may not be the best way to do this...was a nuisance to get running when the service wasn't being run by the 'bindicator' user when ssh'd in, but this seems to work as intended.


