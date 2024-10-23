import sys
import os

# Activate virtual environment
activate_this = '/var/www/flaskapp/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Add the app directory to the sys.path
sys.path.insert(0, '/var/www/flaskapp')

# Import the Flask app
from app import app as application