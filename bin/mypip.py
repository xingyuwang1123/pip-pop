#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Usage:
  pip-diff (--fresh | --stale) <reqfile1> <reqfile2> [--exclude <package>...]
  pip-diff (-h | --help)

Options:
  -h --help     Show this screen.
  --fresh       List newly added packages.
  --stale       List removed packages.
"""


import os
from docopt import docopt
from pip.req import parse_requirements
from pip.index import PackageFinder
from pip._vendor.requests import session

requests=session()

class Requirments(object):
	def __init__(self,reqfile=None):
		super(Requirments,self).__init__()
		self.path=reqfile
		self.requirments=[]
		self.load(reqfile)

	def __repr__(self):
		 return "<requirments: >.format(self.path)"

	def load(self,reqfile):
		 if not os.path.exists(reqfile):
		 	raise ValueError("not exist")

		 finder=PackageFinder([],[],session=requests)
		 for requ in parse_requirements(reqfile,finder=finder,session=session):
		 	self.requirments.append(requ.req)
	def diff(self,requirments,ignore_version=False,exclude=None):
		r1=self
		r2=requirments
		results={'fresh':[],'stale':[]}

		#更新fresh列表
		other_reqs=(
			[r.name for r in r1.requirments]
			if ignore_version else r1.requirments
			)

		for req in r2.requirments:
			r=req.name if ignore_version else req

			if r not in other_reqs and r not in exclude:
				results['fresh'].append(req)

		other_reqs = ([r.name for r in r2.requirments] if ignore_version else r2.requirments)
		for req in r1.requirments:
			r = req.name if ignore_version else req
			if r not in other_reqs and r not in exclude:
				results['stale'].append(req)
		return results


def diff(r1,r2,include_fresh=False,include_stale=False,exclude=None):
	include_versions = True if include_stale else False
	exclude = exclude if len(exclude) else []

	try:
		r1=Requirments(r1)
		r2=Requirments(r2)
	except ValueError:
		print("fail to load in given reqfile")
		exit()

	results=r1.diff(r2,ignore_version=True,exclude=exclude)

	if(include_fresh):
		for line in results['fresh']:
			print(line.name if include_versions  else line)
	if include_stale:
		for line in results['stale']:
			print(line.name if include_versions else line)

def main():
	args = docopt(__doc__, version='pip-diff')
	kwargs={
	'r1': args['<reqfile1>'],
	'r2': args['<reqfile2>'],
	'include_fresh': args['--fresh'],
	'include_stale': args['--stale'],
	'exclude': args['<package>'],
	}

	diff(**kwargs)

if __name__=='__main__':
	main()