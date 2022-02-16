#!/usr/bin/env python3

apikey = ""
port = 8100
serveraddress = "http://localhost:{}/".format(port)
eutils_base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
staticpath = "./static/"
apptitle = "citequery"
retmax = 400
showentrieshtml = 100
showentriesrss = 200
chunksize = 40
cachefile = "./cache/cache.json"
logfile = "./log/log.txt"
examples = {
	"GMDS 2019" : "(Stud Health Technol Inform[jour]) 267[Volume]",
	"E. Garfield in Science" : '(Garfield E[Author]) Science[Journal]',
	"enumerated pmids" : '2695774,10318632,3544508,3531559'
}

