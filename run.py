from crawler import Crawler
import configparser
import os
import sys
import argparse

pn = ''
test_type = test_type = 'Korprov'
bil_type = 'Automatbil'

def extract_args(args, config):
	global pn, test_type, bil_type
	status = False
	if args.pn:
		pn = args.pn
		status = True
	else:
		try:
			pn = config['USER']['pn']
			status = True
		except:
			print("Personnummer not set. Either pass it as an argument or set a default in the config file.")
			return status

	if args.test:
		test_type = args.test
	else:
		try:
			test_type = config['TEST']['type']
		except:
			print('Using default value for test type: Korprov')
			
	status = True

	if args.car:
		bil_type = args.car
	else:
		try:
			bil_type = config['TEST']['car']
		except:
			print('Using default value for car type: Automatbil')
	status = True

	return status
		

# Command line arguments
parser = argparse.ArgumentParser(description='Crawler for trafikverket booking site.')
parser.add_argument('--pn','-p', help='The personnummer of the user.')
parser.add_argument('--test', '-t', help='Test type - Korprov or Kunskapsprov. Default: Korprov')
parser.add_argument('--car', '-c', help='Car type - Automatbil or Manuellbil. Default: Automatbil')
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('config.config')
locs = config['LOCATIONS']['korprov_locs']
status = extract_args(args, config)
if status:
	print(pn)
	c = Crawler(pn=pn, locs=locs, test_type=test_type, bil_type=bil_type)
	c.navigate_no_login()
