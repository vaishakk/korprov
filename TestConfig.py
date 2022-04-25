from crawler import Crawler
import configparser

class TestConfig():
	def __init__(self):
		self.pn = ''
		self.test_type = 'Korprov'
		self.car_type = 'Automatbil'
		self.test_lang = 'English'
		self.loc = ['Farsta']

	def extract_args(self, args, config):
		if args.pn:
			self.pn = args.pn
		else:
			try:
				self.pn = config['USER']['pn']
			except:
				print("Personnummer not set. Either pass it as an argument or set a default in the config file.")
				return False

		if args.test:
			self.test_type = args.test
		else:
			try:
				self.test_type = config['TEST']['type']
			except:
				print('Using default value for test type: %'.format(self.test_type))

		if args.car:
			self.bil_type = args.car
		else:
			try:
				self.bil_type = config['TEST']['car']
			except:
				print('Using default value for car type: %'.format(self.car_type))

		if args.loc:
			self.loc = [args.loc]
		else:
			if self.test_type == 'Korprov':
				try:
					self.loc = config['LOCATIONS']['korprov_locs'].split('\n')
				except:
					print('Using default value for location: %'.format(self.loc))
			else:
				try:
					self.loc = config['LOCATIONS']['kunskap_locs'].split('\n')
				except:
					print('Using default value for location: %'.format(self.loc))

		return True

	def save_config(self, args):
		config = configparser.ConfigParser()
		config.read('config.config')
		if args.pn:
			config['USER']['pn'] = args.pn
		if args.test:
			config['TEST']['type'] = args.test
		if args.car:
			config['TEST']['car'] = args.car
		if args.loc:
			if config['TEST']['type'] == 'Korprov':
				locs  = config['LOCATIONS']['korprov_locs'].split('\n')
				if args.loc not in locs:
					config['LOCATIONS']['korprov_locs'] = config['LOCATIONS']['korprov_locs'] + '\n' + args.loc
			else:
				locs = config['LOCATIONS']['kunskap_locs'].split('\n')
				if args.loc not in locs:
					config['LOCATIONS']['kunskap_locs'] = config['LOCATIONS']['kunskap_locs'] + '\n' + args.loc

		with open('config.config', 'w') as file:
			config.write(file)




