#!/usr/bin/env python
# -*- coding: utf-8 -*-

# used for generating csv files of the bus information

import urllib2

for i in range(6300001,6300013) + range(1000101,1000124):
	req = urllib2.Request('http://www.taipeibus.taipei.gov.tw/Asp/WordPlanAjax.aspx?act=8&townid=%d' % i)
	response = urllib2.urlopen(req)
	content = response.read().split("|")
	for line in content:
		try:
			(name, longitude, latitude) = line.split(",")
		except ValueError:
			continue
		print '"%s","%s,%s"' % (name, longitude, latitude)
