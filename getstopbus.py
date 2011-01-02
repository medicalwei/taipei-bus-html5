#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import cgi

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from django.utils import simplejson

class MainHandler(webapp.RequestHandler):
	def get(self):
		stopName = self.request.get('stopName').encode('utf-8')
		req = urllib2.Request('http://www.taipeibus.taipei.gov.tw/Asp/GetTimeByRouteStop4.aspx?GSName=%s' % stopName)
		response = urllib2.urlopen(req)
		content = response.read().split("|")
		a=[]

		for line in content:
			try:
				(routeName, lon, lat, isReturn, iDontKnowWhatItIs, estTime) = line.split(",")
			except ValueError:
				continue
			routeName=routeName.decode('utf-8').strip(" _")
			isReturn=int(isReturn.strip(" _")) == 1
			estTime=int(estTime.strip(" _"))
			a.append({'routeName': routeName, 'isReturn': isReturn, 'estTime': estTime})

		self.response.out.write(simplejson.dumps(a))

def main():
	application = webapp.WSGIApplication([('/getstopbus', MainHandler)])
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
