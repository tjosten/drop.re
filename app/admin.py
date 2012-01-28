from django.contrib import admin
from app.models import *
from random import random

def generate_invitations(self, request, queryset):
	
	for i in range(0, 9):
		invite = InviteCode(code=random()*100)
		invite.save()

	self.message_user(request, "10 codes generated.")
generate_invitations.short_description = u'Generate 10 codes'

class FileAdmin(admin.ModelAdmin):
	pass

class InviteCodeAdmin(admin.ModelAdmin):
	actions = [generate_invitations]

admin.site.register(File, FileAdmin)
admin.site.register(InviteCode, InviteCodeAdmin)
