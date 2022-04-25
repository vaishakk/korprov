from crawler import Crawler
import configparser
import argparse
from TestConfig import TestConfig


# Command line arguments
parser = argparse.ArgumentParser(description='Crawler for trafikverket booking site.')
parser.add_argument('--pn','-p', help='The personnummer of the user.')
parser.add_argument('--test', '-t', help='Test type - Korprov or Kunskapsprov. Default: Korprov')
parser.add_argument('--car', '-c', help='Car type - Automatbil or Manuellbil. Default: Automatbil')
parser.add_argument('--loc', '-l', help='Location of test. Will be ignored if not a valid location.')
parser.add_argument('--add_config', action='store_true', required=False)
args = parser.parse_args()

test_config = TestConfig()
if args.add_config:
	test_config.save_config(args)
else:
	config = configparser.ConfigParser()
	config.read('config.config')
	status = test_config.extract_args(args, config)
	if status:
		print(test_config.pn)
		c = Crawler(pn=test_config.pn, locs=test_config.loc, test_type=test_config.test_type, bil_type=test_config.bil_type)
		c.navigate_no_login()
