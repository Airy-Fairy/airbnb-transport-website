#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/sharing-wheels-website/")

from wheels import wheels as application
application.secret_key = 'My super secret key'

