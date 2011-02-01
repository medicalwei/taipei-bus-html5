#!/usr/bin/env python

# used to load csv into appengine

from google.appengine.ext import db
from google.appengine.tools.bulkloader import Loader

import models

class StopInfoLoader(Loader):
  def __init__(self):

    def unicode_str(s):
      return s.decode('utf8', 'ignore')
    
    def lat_lon(s):
      lon, lat = [float(v) for v in s.split(',')]
      return db.GeoPt(lat, lon)
    
    Loader.__init__(self, 'StopInfo',
                    [('name', unicode_str),
                     ('location', lat_lon), # set lat and lon
                     ])
  
  def handle_entity(self, entity):
    entity.update_location()
    return entity

loaders = [StopInfoLoader]
