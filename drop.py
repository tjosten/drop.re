import os, sys, urllib2, mimetypes
from django.utils import simplejson

class EnhancedFile(file):
    def __init__(self, *args, **keyws):
        file.__init__(self, *args, **keyws)

    def __len__(self):
        return int(os.fstat(self.fileno())[6])

try:
	filename = sys.argv[1]
except:
	print "usage: python drop.py <filename>"
	sys.exit(0)

filename = 'test.png'

f = EnhancedFile(filename, 'r')
host = "http://drop.re"
url = "%s/up/" % host
headers = {'UP-FILENAME': filename, 'UP-SIZE': len(f), 'UP-TYPE': mimetypes.guess_type(filename)[0], 'UP-COOKIE': '966a84abc00812af53b1cb7d366e8c3d'}

request = urllib2.Request(url, f, headers)
response = urllib2.urlopen(request)
f.close()

for line in response:
	ret = simplejson.loads(line)
	if ret['success'] == True:
		print "URL: %s/%s/" % (host, ret['name'])
		print "Delete: %s/%s/delete/" % (host, ret['delete'])
	else:
		print "Unkown error occurred."

