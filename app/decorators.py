from django.http import Http404, HttpResponse, HttpResponseRedirect
from functools import wraps
from django.core.urlresolvers import reverse
from drop.settings import SECRET

def cookie(func):
	def _check(request, *args, **kwargs):
		try:
			if not request.COOKIES['dorprevip'] == SECRET and not request.META['HTTP_UP_COOKIE'] == SECRET:
				return HttpResponseRedirect(reverse('no-sorry'))
			else:
				return func(request, *args, **kwargs)
		except:
			return HttpResponseRedirect(reverse('no-sorry'))

	return wraps(func)(_check)