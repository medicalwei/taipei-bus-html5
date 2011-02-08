#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from django.utils import simplejson
from operator import itemgetter

class RouteInfo(db.Model):
	routeName = db.StringProperty()
	isReturn = db.IntegerProperty()
	stopName = db.StringProperty()
	nextStopName = db.StringProperty()

class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers.add_header("Cache-Control", "no-cache")
		stopName = self.request.get('stopName')
		response = urlfetch.fetch('http://www.taipeibus.taipei.gov.tw/Asp/GetTimeByRouteStop4.aspx?GSName=%s' % stopName.encode('utf-8'), deadline=10).content
		content = response.split("|")
		busLines=[]

		for line in content:
			try:
				(routeName, lon, lat, isReturn, iDontKnowWhatItIs, estTime) = line.split(",")
			except ValueError:
				continue

			routeName=routeName.strip(" _").decode('utf-8')
			isReturn=int(isReturn.strip(" _"))
			estTime=int(estTime.strip(" _"))

			try: 
				nextStopName = RouteInfo.gql( "WHERE routeName = :1 "
							"AND isReturn = :2 "
							"AND stopName = :3 "
							"LIMIT 1",
							routeName,
							isReturn,
							stopName)[0].nextStopName
			except IndexError:
				nextStopName = "unknown"
				

			# mark those which < 0 as unknown
			if estTime<0:
				estTime=86400

			busLines.append({'routeName': routeName, 'nextStopName': nextStopName, 'estTime': estTime})

		# sort the lines
		busLines = sorted(busLines,key=itemgetter('estTime'))

		# encapsulize
		data = {'requestName': stopName, 'content': busLines}

		# send data
		self.response.out.write(simplejson.dumps(data))




def main():
	application = webapp.WSGIApplication([('/getstopbus', MainHandler)])
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
