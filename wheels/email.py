from __future__ import print_function
import sys

from wheels import WHEELS_MAIL_SENDER, WHEELS_MAIL_SUBJECT_PREFIX, mail
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(to, subject, template, **kwargs):
	app = current_app._get_current_object()
	msg = Message(WHEELS_MAIL_SUBJECT_PREFIX + ' ' + subject,
				  sender=WHEELS_MAIL_SENDER, recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr
