import sys
import logging

# Add your project directory to the sys.path
sys.path.insert(0, '/var/www/flaskapp')

# Activate the virtual environment
activate_this = '/var/www/flaskapp/venv/bin/activate'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import app as application  # Import your Flask application