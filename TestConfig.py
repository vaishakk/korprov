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
					self.loc = config['LOCATIONS']['korprov_locs']
				except:
					print('Using default value for location: %'.format(self.loc))
			else:
				try:
					self.loc = config['LOCATIONS']['kunskap_locs']
				except:
					print('Using default value for location: %'.format(self.loc))

		return True