#!/usr/bin/env python3

from json import loads, dumps
from json.decoder import JSONDecodeError

_printf = lambda mes,*parms: print(mes.format(*parms),flush=True)

class CachedDict(dict):
	def __init__(self,filename,verbose=False):
		self.filename = filename
		self.verbose = verbose
		self.load()
	def load(self): 
		try:
			self.update(**loads(open(self.filename).read()))
			if self.verbose:
				_printf("{} records(s) read from {}.",
					len(self.items()),self.filename),
		except (FileNotFoundError,JSONDecodeError):
			if self.verbose:
				_printf("No records read from {}.",
					self.filename)
	def save(self):
		with open(self.filename,"w+") as f:
			f.write(dumps({k:v for k,v in self.items()}))
		if self.verbose:
			_printf("{} record(s) written to {}.",
				len(self.items()),self.filename)

