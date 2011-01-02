#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import urllib2

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from geo.geomodel import GeoModel
import geo.geotypes
from django.utils import simplejson

class StopInfo(GeoModel):
	name = db.StringProperty()

class MainHandler(webapp.RequestHandler):
	def get(self):
		lon = float(self.request.get('lon'))
		lat = float(self.request.get('lat'))
		accuracy = float(self.request.get('accuracy'))
		if accuracy < 250:
			accuracy = 250
		elif accuracy > 2000:
			accuracy = 2000

		results = StopInfo.proximity_fetch( StopInfo.all(),
		                                    geo.geotypes.Point(lat, lon),
		                                    max_results=30, max_distance=accuracy)
		
		stops=[]
		for entity in results:
			stops.append(entity.name);

		self.response.out.write(simplejson.dumps(stops))



def main():
	application = webapp.WSGIApplication([('/getstops', MainHandler)], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
