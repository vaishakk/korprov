from crawler import Crawler
import configparser
import os
import sys

config = configparser.ConfigParser()
config.read('config.config')
pn = ''
if len(sys.argv) > 1:
	pn = sys.argv[1]
else:
	pn = config['USER']['pn']

try:
	test_type = config['TEST']['type']
except:
	test_type = 'Korprov'

locs = []
if test_type == 'Korprov':
	loc_str = 'korprov_locs'
else:
	loc_str = 'kunskap_locs'
try:
	locs = config['LOCATIONS'][loc_str].split('\n')
except:
	locs = []

try:
	bil_type = config['TEST']['car']
except:
	bil_type = 'Automatbil'


print(pn)
c = Crawler(pn=pn, locs=locs, test_type=test_type, bil_type=bil_type)
c.navigate_no_login()
