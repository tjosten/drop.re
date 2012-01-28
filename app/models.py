from django.db import models
from settings import SAVE_PATH, APP_URL
from datetime import datetime
from random import random

class File(models.Model):
	file = models.FileField(upload_to=SAVE_PATH, max_length=255)
	pub_date = models.DateTimeField()
	secret = models.CharField(max_length=255, blank=False, null=False)
	name = models.CharField(max_length=255, blank=False, null=False)
	type = models.CharField(max_length=255, blank=False, null=False)
	download_cnt = models.BigIntegerField(null=True, blank=True)

	def __unicode__(self):
		return "%s - %s" % (self.pub_date, self.file.name)

def generate_invite_code():
	return random()*100

class InviteCode(models.Model):
	code = models.CharField(max_length=255, blank=False, null=False, default=generate_invite_code)

	def __unicode__(self):
		return "%s/%s/invite/" % (APP_URL, self.code)