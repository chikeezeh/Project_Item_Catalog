#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/FlaskApp2/")

from FlaskApp2 import app as application  # noqa
application.secret_key = 'Add your secret key'
