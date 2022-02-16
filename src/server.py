#!/usr/bin/env python3

"""

by Dennis Toddenroth, 2022

start with: 
nohup python3 server.py > nohup.out 2>&1 & echo $! > pid.txt

stop with: 
kill -s SIGTERM $(<pid.txt)

kill with: 
kill -s SIGKILL $(<pid.txt)

"""

from json import dumps
from urllib.parse import quote_plus
import logging

from web import route, servestatic, run
from helpers import formatrssdate
from queryapi import pubmedsearch, pubmedcitations,\
	cachedpubmedrecords, writecache
import config
import templates

logging.basicConfig(filename=config.logfile,level=logging.INFO)

def _sortcitations(citations,records):
	flattened = sum([list((citing,int(target)) for citing in citations)
		for target, citations in citations.items()],[])
	flattened.sort(key=lambda entry: records.get(str(entry[0])
		).get("pubdate"),reverse=True)
	return flattened

@route("/api","application/json")
def api(query="",maxres=config.showentriesrss,**kwargs):
	pmids = pubmedsearch(query)["pmids"] if len(query) else []
	citations = pubmedcitations(pmids)
	allpmids = pmids + sum(citations.values(),[])
	records = cachedpubmedrecords(allpmids)
	flattened = _sortcitations(citations,records)
	return dumps([dict(citing=citation[0],cited=citation[1]) 
		for citation in flattened])

@route("/rss","application/rss+xml")
def api(query="",maxres=config.showentriesrss,**kwargs):
	pmids = pubmedsearch(query)["pmids"] if len(query) else []
	citations = pubmedcitations(pmids)
	allpmids = pmids + sum(citations.values(),[])
	records = cachedpubmedrecords(allpmids)
	flattened = _sortcitations(citations,records)
	items = ""
	for citing,cited in flattened[:maxres]:
		record_citing = records.get(str(citing))
		text_citing = templates.citationtext.format(**record_citing)
		text_cited = templates.citationtext.format(
			**records.get(str(cited)))
		description = templates.rssdescription.format(
			title=record_citing["title"],pmid=citing,
			abstract=record_citing["abstract"],
			citing=text_citing,cited=text_cited)
		pubdate = formatrssdate(record_citing["pubdate"])
		items += templates.rssitem.format(title=record_citing["title"],
			description=description,
			pmid=citing,author=text_citing,
			itemid="{}:{}".format(citing,cited),
			pubDate=pubdate)
	return templates.rssframe.format(query=query,items=items,
		serveraddress=config.serveraddress)

@route("/search","text/html")
def mainquery(query="",maxres=config.showentrieshtml,**kwargs):
	status = templates.examples.format(examples=", ".join(
		["<a href='/search?query="+quote_plus(v)+"'>"
		+k+"</a>" for k,v in config.examples.items()]))
	pmids = pubmedsearch(query)["pmids"] if len(query) else []
	citations = pubmedcitations(pmids)
	ncitations = len(sum(citations.values(),[]))
	if ncitations>0:
		status = templates.resultfreqs.format(
			ncitations=ncitations,query=query,
			ncited=len(list(citations.keys())))
	allpmids = pmids + sum(citations.values(),[])
	records = cachedpubmedrecords(allpmids)
	flattened = _sortcitations(citations,records)
	results = ""
	for citing,cited in flattened[:maxres]:
		citation_citing = templates.citing.format(
			**records.get(str(citing)))
		citation_cited = templates.cited.format(
			**records.get(str(cited)))
		results += templates.citation.format(
			citing=citation_citing,cited=citation_cited)
	content = templates.mainform.format(query=query,
		status=status,results=results)
	return templates.index.format(caption=config.apptitle,
		content=content,layout="showresults")

@route("/","text/html")
def main(**kwargs):
	status = templates.examples.format(examples=", ".join(
		["<a href='/search?query="+quote_plus(v)+"'>"
		+k+"</a>" for k,v in config.examples.items()]))
	content = templates.mainform.format(query="",
		status=status,results="")
	return templates.index.format(caption=config.apptitle,
		content=content,layout="showform")

@route("/favicon.ico","image/x-icon")
def favicon(**kwargs):
	return open(config.staticpath + "favicon.ico","rb").read()

# make nohup-operation controllable: 
def _termhandler(signum,frame):
	from sys import exit
	print("Received SIGTERM, shutting down...",flush=True)
	writecache()
	exit()
from signal import signal, SIGTERM
signal(SIGTERM,_termhandler)

if __name__=='__main__':
	servestatic(config.staticpath)
	print(f"Starting server on port {config.port}.",flush=True)
	print(f"Visit http://localhost:{config.port}/",flush=True)
	try:
		run(port=config.port)
	except KeyboardInterrupt:
		print("\nShutting down")
		writecache()

