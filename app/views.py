#coding: utf8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from datetime import datetime
from urllib import urlencode
from urllib2 import urlopen
from django.core.files.base import ContentFile
from django.utils import simplejson
from random import random
from settings import MAX_UPLOAD_SIZE, APP_URL

from drop.settings import *
from drop.app.models import *

from decorators import cookie

def no_view(request):
	try:
		if request.COOKIES['dorprevip'] == "966a84abc00812af53b1cb7d366e8c3d":
			return HttpResponseRedirect(reverse("default"))
	except:
		pass
	return render_to_response("no.html", locals(), context_instance=RequestContext(request))

@cookie
def default_view(request):
	app_url = APP_URL
	cookie = request.COOKIES['dorprevip']
	return render_to_response("default.html", locals(), context_instance=RequestContext(request))

@cookie
def up_view(request):
	content = request.raw_post_data
	response = False
	if not content:
		response = {'success': False, 'message': 'Empty file!'}
		return HttpResponse(simplejson.dumps(response))

	try:
		contentFile = ContentFile(content)
		contentFile.name = request.META['HTTP_UP_FILENAME']
		contentFile.type = request.META['HTTP_UP_TYPE']

		if int(contentFile.size) > MAX_UPLOAD_SIZE:
			response = {'success' : False, 'error' : 'File is too big!'}
			raise

		f = File(pub_date=datetime.now(), secret=random()*100, name=random()*100, type=contentFile.type)
		f.file.save(contentFile.name, contentFile)
		f.save()		
		f = File.objects.get(pk=f.pk)
		response = {'success': True, 'name': f.name, 'delete': f.secret}
	except:
		if not response:
			response = {'success': False, 'error': 'Upload failed!'}

	return HttpResponse(simplejson.dumps(response))

def down_view(request, file):
	f = get_object_or_404(File, Q(name=file))
	if not f.download_cnt:
		f.download_cnt = 1
	else:
		f.download_cnt+=1
	f.save()
	response = HttpResponse(mimetype=f.type)
	response['Content-Length'] = f.file.size
	response.write(f.file.read())
	return response

def delete_view(request, file):
	f = get_object_or_404(File, Q(secret=file))
	f.delete()
	messages.add_message(request, messages.SUCCESS, 'File deleted!')
	return HttpResponseRedirect(reverse("default"))