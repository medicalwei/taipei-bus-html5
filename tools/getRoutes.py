#!/usr/bin/env python
# -*- coding: utf-8 -*-

# used for generating csv files of the bus information

import urllib2
import re

req = urllib2.Request('http://5284.taipei.gov.tw/WordPlan/WordBus.aspx?Lang=cht')
response = urllib2.urlopen(req)
routes = map(lambda x: x.strip('\''), re.search('\[(.*)\]', response.readline()).group(1).split(","))

for route in routes:
	req = urllib2.Request('http://5284.taipei.gov.tw/Asp/start21.aspx?Glid=%s' % (route))
	response = urllib2.urlopen(req)
	stops = response.readline().split("&")[0].split("|")
	
	lastStop=[]
	for stop in stops:
		try:
			(name, noUseA, noUseB, isReturn, noUseC) = stop.split(",")
		except ValueError:
			continue	

		name=name.strip(" _")
		isReturn=int(isReturn.strip(" _"))

		if lastStop:
			print '"%s",%s,"%s","%s"' % (route,lastStop[1], lastStop[0], name)

		lastStop=[name, isReturn]

	
