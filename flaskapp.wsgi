import sys
import os

# Add the virtual environment's site-packages to the sys.path
sys.path.insert(0, '/var/www/flaskapp/venv/lib/python3.10/site-packages')

# Add the app directory to the sys.path
sys.path.insert(0, '/var/www/flaskapp')

# Import the Flask app
from app import app as application