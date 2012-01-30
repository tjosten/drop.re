from django.http import Http404, HttpResponse, HttpResponseRedirect
from functools import wraps
from django.core.urlresolvers import reverse
from drop.settings import SECRET

def cookie(func):
	def _check(request, *args, **kwargs):
		try:
			try:
				if request.COOKIES['dorprevip'] == SECRET:
					return func(request, *args, **kwargs)
			except KeyError, NameError:		
				try:
					if request.META['HTTP_UP_COOKIE'] == SECRET:
						return func(request, *args, **kwargs)
				except KeyError, NameError:
					raise
			raise
		except:
			return HttpResponseRedirect(reverse('no-sorry'))

	return wraps(func)(_check)