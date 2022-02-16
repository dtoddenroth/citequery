#!/usr/bin/env python3

from json import loads, dumps
from json.decoder import JSONDecodeError

class CachedDict(dict):
	def __init__(self,filename,verbose=False):
		self.filename = filename
		self.verbose = verbose
		self.load()
	def load(self): 
		try:
			self.update(**loads(open(self.filename).read()))
			if self.verbose:
				print("{} records(s) read from {}.".format(
					len(self.items()),self.filename),
					flush=True)
		except (FileNotFoundError,JSONDecodeError):
			if self.verbose:
				print("No records read from {}.".format(
					self.filename),
					flush=True)
	def save(self):
		with open(self.filename,"w+") as f:
			f.write(dumps({k:v for k,v in self.items()}))
		if self.verbose:
			print("{} record(s) written to {}.".format(
				len(self.items()),self.filename),
				flush=True)
