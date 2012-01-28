from django.contrib import admin
from app.models import *

class FileAdmin(admin.ModelAdmin):
	pass

admin.site.register(File, FileAdmin)
