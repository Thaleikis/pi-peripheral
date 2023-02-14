#!/bin/bash

# Enable neccessary modules
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
echo "libcomposite" | sudo tee -a /etc/modules

# Copy needed Software
sudo cp isticktoit_usb /usr/bin
sudo chmod +x /usr/bin/isticktoit_usb

sed -i '$i/usr/bin/isticktoit_usb' /etc/rc.local

# Enable service
sudo cp ../piperipheral.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable piperipheral.service
sudo systemctl start piperipheral.service

# Create Cronjob to update project repository once a Minute
crontab -u pi -l > pi_cron  # Backup existing crontab for pi
echo "* * * * * cd /home/pi/pi-peripheral && git pull > /dev/null 2>&1" >> pi_cron  # Add new cronjob
crontab -u pi pi_cron  # Install new crontab
rm pi_cron  # Remove backup file
