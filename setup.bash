#!/bin/bash
sudo apt-get update
sudo apt install python3 python3-pip apache2 libapache2-mod-wsgi-py3 -y

sudo apt-get install python3-venv
sudo cp flaskapp.conf /etc/apache2/sites-available/flaskapp.conf

sudo mkdir /var/www/flaskapp
sudo chown -R $USER:$USER /var/www/flaskapp
sudo cp app.py /var/www/flaskapp/
sudo cp flaskapp.wsgi /var/www/flaskapp/
cd /var/www/flaskapp
python3 -m venv venv
source venv/bin/activate
pip install flask openai requests beautifulsoup4
sudo chown -R www-data:www-data /var/www/flaskapp
sudo a2ensite flaskapp
sudo systemctl restart apache2