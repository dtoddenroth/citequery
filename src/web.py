#!/usr/bin/env python3

"""
Bottle-style decorator for exposing functions via class-based tornado handlers, 
which may support concurrency. Right now only supports 'get'. 

by Dennis Toddenroth, 2022

Usage: 

from random import random
from json import dumps
from web import route, run

@route("/","application/json")
def numbers(**kwargs):
	return dumps(dict(rand=random(),**kwargs))
run()

"""

import logging
from urllib.parse import unquote
from mimetypes import _types_map_default as mimemap
from tornado import web, httpserver, ioloop

class Router():
	def __init__(self):
		self.routes = dict()
	def addroute(self,matcher,method):
		handler = type('Handler' + method.__name__, 
			(web.RequestHandler,), {'get': method})
		self.routes[matcher] = handler
	def getroutes(self):
		return list(self.routes.items())

_myrouter = Router()

def route(matcher="/",mime=None):
	def route_decorator(method):
		_localmethod = method
		_mime = mime
		def _handler(self):
			if not _mime is None:
				self.set_header("Content-Type", _mime)
			args = {k: v[0].decode()
				for k,v in self.request.arguments.items()}
			self.write(_localmethod(**args))
		_myrouter.addroute(matcher,_handler)
		return method
	return route_decorator

def servestatic(localdir,matcher="/static/.*"):
	def _handler(self):
		localfile = localdir + self.request.path[-len(matcher)+1:]
		mime = mimemap.get("."+localfile.split(".")[-1],"text/plain")
		try: 
			self.set_header("Content-Type", mime)
			self.write(open(localfile,"rb").read())
		except FileNotFoundError:
			self.set_header("Content-Type", "text/plain")
			self.set_status(404,"Not available")
			logging.info("Static file not found: {}".format(
				localfile))
			self.write("File not found")
	_myrouter.addroute(matcher,_handler)

def run(port=80):
	global _server
	app = web.Application(_myrouter.getroutes())
	server = httpserver.HTTPServer(app)
	server.listen(port)
	ioloop.IOLoop.current().start()

def _demo(port=8200):
	from random import random
	from json import dumps
	@route("/","application/json")
	def numbers(x=1,y=2,**kwargs):
		return dumps(dict(rand=random(),xandy=int(x)+int(y),**kwargs))
	print("http://localhost:%s/?hello=world shows some numbers. " % port)
	run(port)

if __name__=='__main__':
	_demo()
