from google.appengine.ext import db
from geo.geomodel import GeoModel

class StopInfo(GeoModel):
	name = db.StringProperty()

class RouteInfo(db.Model):
	routeName = db.StringProperty()
	isReturn = db.IntegerProperty()
	stopName = db.StringProperty()
	nextStopName = db.StringProperty()

