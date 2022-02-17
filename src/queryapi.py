#!/usr/bin/env python3

from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen
from urllib.error import URLError
from lxml.etree import fromstring
import logging

from config import eutils_base, retmax, cachefile, chunksize, apikey
from cacheddict import CachedDict
from helpers import chunkedmap, unicodedict2entities

_pmcache = CachedDict(cachefile,True)
el2int = lambda el: int(el.text)
getids = lambda el: list(map(el2int,[] if el is None else el.findall(".//Id")))

def article2authorcaption(article):
	authors = article.findall(".//Author")
	if len(authors)<1:
		return ""
	firstauthor = authors[0].find("./LastName").text\
		if not authors[0].find("./LastName") is None else "N.N."
	return firstauthor + (" et al." if len(authors)>1 else "")

def article2date(article):
	for xpath in [".//ArticleDate",".//PubDate",".//PubMedPubDate"]:
		try:
			pubdate = "{}-{:02d}-{:02d}".format(*list(
				map(int,article.find(xpath).itertext()))[:3])
			if len(pubdate)==10:
				return pubdate
		except:
			pass
	return article.find(".//PubMedPubDate/Year").text

def article2abstract(article):
	abstractel = article.find(".//Abstract")
	return "" if abstractel is None else " ".join(abstractel.itertext())

def article2dict(article):
	pubdate = article2date(article)
	return dict(pmid=el2int(article.find(".//PMID")),
		title=" ".join(article.find(".//ArticleTitle").itertext()),
		abstract=article2abstract(article),
		authors=article2authorcaption(article),
		pubdate=pubdate,
		journal=article.find(".//Journal/ISOAbbreviation").text,
		year=int(pubdate[:4]))

def queryandparse(utility,moregetparms="",**queryparms):
	if len(apikey):
		queryparms.update(api_key=apikey)
	url = eutils_base+utility+"?"+urlencode(
		queryparms,quote_via=quote_plus)+moregetparms
	queryparms.update(api_key="XXXXXXX")
	displayurl = eutils_base+utility+"?"+urlencode(
		queryparms,quote_via=quote_plus)+moregetparms	
	try:
		logging.info(f"Querying {displayurl}...")
		return fromstring(urlopen(url).read())
	except URLError:
		logging.error(f"Error fetching from {displayurl}")
	
def pubmedsearch(query,retmax=retmax):
	queryparms = dict(db="pubmed",term=query,retmax=retmax,retmode="xml")
	etree = queryandparse("esearch.fcgi",**queryparms)
	if etree is None:
		return dict(count=0,pmids=[])
	return dict(count=el2int(etree.find("./Count")),
		pmids=getids(etree.find(".//IdList")))

def pubmedcitations(pmids,retmax=retmax):
	queryparms = dict(dbfrom="pubmed",linkname="pubmed_pubmed_citedin",
		retmax=retmax,retmode="xml")
	def citationchunk(localpmids):
		moregetparms = "".join([f"&id={pmid}" for pmid in localpmids])
		etree = queryandparse("elink.fcgi",moregetparms,**queryparms)
		if etree is None:
			return []
		return [(el2int(linkset.find(".//IdList/Id")), 
	 		getids(linkset.find(".//LinkSetDb")))
	 		for linkset in etree.findall(".//LinkSet")]
	rows = chunkedmap(citationchunk,pmids,chunksize)
	return {row[0]:row[1] for row in rows}

def chunkedpubmedrecords(pmids):
	def pubmedrecords(pmids):
		queryparms = dict(db="pubmed",retmode="xml",
			id=",".join(map(str,pmids)))
		etree = queryandparse("efetch.fcgi",**queryparms)
		if etree is None:
			return []
		return list(map(article2dict,
			etree.findall(".//PubmedArticle")))
	return chunkedmap(pubmedrecords,pmids,chunksize)
		
def cachedpubmedrecords(pmids):
	pmidstrs = list(map(str,pmids))
	missingpmids = [pmid for pmid in pmidstrs if not pmid in _pmcache]
	cachedpmids = [pmid for pmid in pmidstrs if pmid in _pmcache]
	records = []
	if len(missingpmids):
		records = chunkedpubmedrecords(missingpmids)
		_pmcache.update({str(el["pmid"]):el for el in records})
	records += [_pmcache.get(pmid) for pmid in cachedpmids]
	return {str(record.get("pmid")): unicodedict2entities(record)
		for record in records}

def writecache():
	_pmcache.save()
