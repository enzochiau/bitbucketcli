import logging
import requests
import os
import sys
import getpass
import json
import imp
import argparse
from os.path import expanduser
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne


class Repolist(Lister):
	log = logging.getLogger(__name__ + '.Repolist')

	def take_action(self, parsed_args):
		home = expanduser("~")
		filename = os.path.join(home, '.bitbucket.py')
		creds = imp.load_source('.bitbucket', filename)
		user = creds.username
		passwd = creds.passwd
		url = "https://bitbucket.org/api/1.0/user/repositories/"
		r = requests.get(url, auth=(user, passwd))
		data = json.loads(r.text)
		return (('Owner', 'Repo Name', 'Created On' ),
			((i['owner'], i['name'], i['created_on']) for i in data)
			)

class Repodetail(ShowOne):
	log = logging.getLogger(__name__ + '.Repodetail')

	def get_parser(self, prog_name):
		parser = super(Repodetail, self).get_parser(prog_name)
		parser.add_argument('--reponame', '-r', metavar='<reponame>', help='The repository name')
		return parser

	def take_action(self, parsed_args):
		home = expanduser("~")
		filename = os.path.join(home, '.bitbucket.py')
		creds = imp.load_source('.bitbucket', filename)
		user = creds.username
		passwd = creds.passwd
		url = "https://bitbucket.org/api/1.0/user/repositories/"		
		r = requests.get(url, auth=(user, passwd))
		data = json.loads(r.text)
		for i in data:
			if i['name'] == parsed_args.reponame:
				columns = i.viewkeys()
				data = i.viewvalues()
		return (columns, data)

