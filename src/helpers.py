#!/usr/bin/env python3

from datetime import date

_unicode2entities = lambda s: str(s).replace("&","&amp;").replace(">","&gt;"
	).replace("<","&lt;").encode('ascii','xmlcharrefreplace').decode()

def unicodedict2entities(d):
	return {k:_unicode2entities(v) for k,v in d.items()}

def chunkedmap(func,inputs,chunksize):
	chunks = list(range((len(inputs)-1)//chunksize+1))
	return sum([func(inputs[chunk*chunksize:(chunk+1)*chunksize]) 
		for chunk in chunks],[])

def formatrssdate(pmdate):
	try: 
		year,month,day = list(map(int,pmdate.split("-")))
		return date(year,month,day).strftime("%a, %d %b %Y")
	except:
		return pmdate

