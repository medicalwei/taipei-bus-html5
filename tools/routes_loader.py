#!/usr/bin/env python

# used to load csv into appengine

from google.appengine.ext import db
from google.appengine.tools.bulkloader import Loader

import models

class RouteInfoLoader(Loader):
  def __init__(self):

    def unicode_str(s):
      return s.decode('utf8', 'ignore')
    
    Loader.__init__(self, 'RouteInfo',
                    [('routeName', unicode_str),
                     ('isReturn', int), # set lat and lon
                     ('stopName', unicode_str), # set lat and lon
                     ('nextStopName', unicode_str) # set lat and lon
                     ])

loaders = [RouteInfoLoader]
