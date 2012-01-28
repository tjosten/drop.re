from django.conf.urls.defaults import patterns, include, url
from drop.settings import MEDIA_ROOT

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': False }),
	url('^$', 'app.views.default_view', name="default"),
	url('^fuckyou/$', 'app.views.no_view', name="no-sorry"),
	url('^up/$', 'app.views.up_view', name="up"),
	url('^(?P<file>[0-9]{1,3}\.[0-9]+)/$', 'app.views.down_view', name="down"),
	url('^(?P<file>[0-9]{1,3}\.[0-9]+)/delete/$', 'app.views.delete_view', name="delete"),
	url(r'^admin/', include(admin.site.urls)),
)
