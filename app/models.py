from django.db import models
from settings import SAVE_PATH

class File(models.Model):
	file = models.FileField(upload_to=SAVE_PATH, max_length=255)
	pub_date = models.DateTimeField()
	secret = models.CharField(max_length=255, blank=False, null=False)
	name = models.CharField(max_length=255, blank=False, null=False)
	type = models.CharField(max_length=255, blank=False, null=False)
	download_cnt = models.BigIntegerField(null=True, blank=True)

	def __unicode__(self):
		return "%s - %s" % (self.pub_date, self.name)