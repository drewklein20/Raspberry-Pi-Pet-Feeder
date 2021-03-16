#!/bin/bash

sudo mysql
USE FEEDER;
CREATE USER 'remote'@'localhost' IDENTIFIED BY 'PetFeeder2021!';
CREATE USER 'remote'@'%' IDENTIFIED BY 'PetFeeder2021!';
GRANT ALL PRIVILEGES ON * . * TO 'remote'@'localhost';
GRANT ALL ON *.* TO 'remote'@'%';
FLUSH PRIVILEGES;
exit;


sudo rm -rf /var/www/html/*
sudo cp -r dist/* /var/www/html/
sudo mkdir /var/www/html/php
sudo cp -r php/* /var/www/html/php/
sudo chown -R www-data:www-data /var/www/
sudo usermod -aG www-data pi
addgroup www-data
sudo chown -R www-data:www-data /var/www/html/*
sudo chmod -R 770 /var/www/ /var/www/html/*
sudo rm /lib/systemd/system/scale.service
sudo rm /lib/systemd/system/alexa.service
sudo cp *.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/scale.service
sudo chmod 644 /lib/systemd/system/alexa.service
sudo chmod +x /var/www/html/php/scale.py
sudo chmod +x /var/www/html/php/feed.py
sudo chmod +x /var/www/html/php/alexaFeed.py
sudo systemctl daemon-reload
sudo systemctl enable alexa.service
sudo systemctl enable scale.service
sudo systemctl start alexa.service
sudo systemctl start scale.service