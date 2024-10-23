#!/bin/bash
sudo apt-get update
sudo apt-get install apache2 libapache2-mod-wsgi-py3 python3-pip
pip3 install flask openai requests beautifulsoup4

sudo mkdir -p /var/www/flaskapp
sudo chmod -R 755 /var/www/flaskapp
sudo cp app.py /var/www/flaskapp/
sudo cp flaskapp.wsgi /var/www/flaskapp/

sudo chown -R www-data:www-data /var/www/flaskapp
sudo cp flaskapp.conf /etc/apache2/sites-available/flaskapp.conf
sudo a2ensite flaskapp
sudo a2dissite 000-default
sudo apache2ctl configtest
sudo service apache2 restart
