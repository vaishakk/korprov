import configparser
import os

class TestConfig():
	def __init__(self, config_file):
		config = configparser.ConfigParser()
		if os.path.exists(config_file):
			config.read(config_file)
		else:
			with open(config_file, 'w') as file:
				file.write('[USER]\n[TEST]\n[LOCATIONS]') 
		try:
			self.pn = config['USER']['pn']
		except:
			self.pn = ''
		try:
			self.test_type = config['TEST']['type']
		except:
			self.test_type = 'Korprov'
		try:
			self.bil_type = config['TEST']['car']
		except:
			self.car_type = 'Automatbil'
		try:
			self.language = config['TEST']['language']
		except:
			self.language = 'Engelska'
		if self.test_type == 'Korprov':
			try:
				self.loc = config['LOCATIONS']['korprov_locs'].split('\n')
			except:
				self.loc = []
		else:
			try:
				self.loc = config['LOCATIONS']['kunskap_locs'].split('\n')
			except:
				self.loc = []

	def extract_args(self, args):
		if args.pn:
			self.pn = args.pn
		elif self.pn == '':
			print("Personnummer not set. Either pass it as an argument or set a default in the config file.")
			return False

		if args.test:
			self.test_type = args.test

		if self.test_type == 'Korprov':
			if args.car:
				self.bil_type = args.car

		if self.test_type == 'Kunskapsprov':
			if args.lang:
				self.language = args.lang

		if args.loc:
			self.loc = [args.loc]
		
		if not self.loc:
			print('Scanning all locations.')

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
		if args.lang:
			config['TEST']['language'] = args.lang
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

	def show_config(self):
		print('Personnummer: {}'.format(self.pn))
		print('Test Type: {}'.format(self.test_type))
		if self.test_type == 'Korprov':
			print('Car Type: {}'.format(self.bil_type))
		else:
			print('Test language: {}'.format(self.language))
		print('Test locations: {}'.format(self.loc))
