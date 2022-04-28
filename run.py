from crawler import Crawler
import configparser
import argparse
from TestConfig import TestConfig

CONFIG_FILE = 'config.config'
# Command line arguments
parser = argparse.ArgumentParser(description='Crawler for trafikverket booking site.')
parser.add_argument('--pn','-p', help='The personnummer of the user.')
parser.add_argument('--test', '-t', help='Test type - Korprov or Kunskapsprov. Default: Korprov')
parser.add_argument('--car', '-c', help='Car type - Automatbil or Manuellbil. Default: Automatbil. Only valid for Korprov.' )
parser.add_argument('--loc', '-l', help='Location of test. Will be ignored if not a valid location.')
parser.add_argument('--lang', '-s', help='Language of test. Default: Engelska. Only valid for Kunskapsprov')
parser.add_argument('--add_config', action='store_true', required=False)
parser.add_argument('--show_config', action='store_true', required=False)
args = parser.parse_args()

test_config = TestConfig(CONFIG_FILE)
if args.add_config:
	test_config.save_config(args)
elif args.show_config:
	test_config.show_config()
else:
	status = test_config.extract_args(args, CONFIG_FILE)
	if status:
		print(test_config.pn)
		c = Crawler(test_config)
		c.navigate_no_login()
