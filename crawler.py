from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import configparser
from TestConfig import TestConfig
import os
import sys

CAR_TYPE = {
	'Automatbil': '4',
	'Manuellbil': '2'
}

LANGUAGE = {
	'Tyska': "12",
	'Turkiska': "11",
	'Thailändska': "133",
	'Spanska': "10",
	'Sorani': "9",
	'Somaliska': "128",
	'Ryska': "8",
	'Persiska': "7",
	'Franska': "6",
	'Finska': "5",
	'Engelska': "4",
	'BKS': "3",
	'Arabiska': "2",
	'Albanska': "1",
	'Svenska': "13",
}


class Crawler(webdriver.Chrome):
	def __init__(self, test_config):
		service = Service('./chromedriver')
		super().__init__(service=service)
		self.config = test_config
		if not len(self.config.loc):
			if self.config.test_type == 'Korprov':
				with open('korprov-locs.txt','r') as file:
					for loc in file.readlines():
						self.config.loc.append(loc.strip())
			else:
				with open('kunskaps-locs.txt','r') as file:
					for loc in file.readlines():
						self.config.loc.append(loc.strip())

		self.iterator, self.out_file = (self.iter_locs_korprov, 'korprov-times.csv') if self.config.test_type == 'Korprov' \
								  else (self.iter_locs_kunskapsprov, 'kunskaps-times.csv')

	def navigate_no_login(self):
		self.get("https://fp.trafikverket.se/Boka/#/licence/")
		self.implicitly_wait(10)
		# Input personnummer
		ssn = self.find_element(By.ID, 'social-security-number-input')
		ssn.send_keys(self.config.pn)
		# Select B
		opts = self.find_elements(By.CLASS_NAME,'list-group-item')
		opts[3].click()
		# Wait for page to load
		# WebDriverWait(self, timeout=3).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'form-control')) == 7)
		with open(self.out_file,'w') as file:
			for l, t in self.iterator():
				file.write('{}, {}\n'.format(l, t))
				print(l + '>' + t)
		self.close()

	def navigate_with_login(self):
		self.get("https://fp.trafikverket.se/Boka/#/")
		self.implicitly_wait(10)
		# Click 'Mina prov' button
		buttons = self.find_elements(By.CLASS_NAME, 'col-sm-3')
		buttons[1].click()
		self.implicitly_wait(10)
		# Input personnummer
		ssn = self.find_element(By.ID, 'social-security-number-input')
		ssn.send_keys(pn)
		# Click 'Continue'
		cont = self.find_elements(By.CLASS_NAME, 'col-sm-4.col-sm-offset-3.col-sm-push-2')
		cont[0].click()
		self.implicitly_wait(10)
		# Wait for page to load
		WebDriverWait(self, timeout=30).until(lambda d: d.find_elements(By.CLASS_NAME, 'col-sm-3')[1].is_displayed())
		self.implicitly_wait(10)
		# Click 'Mina prov' button
		clicked = False
		while not clicked:
			try:	
				self.find_elements(By.CLASS_NAME, 'col-sm-3')[1].click()
			except:
				pass
			else:
				clicked = True
		panel = self.find_elements(By.CLASS_NAME, 'panel.panel-success')[0]
		panel.find_elements(By.XPATH,"//*[contains(text(), 'Omboka')]")[0].click()
		with open('korprov-times.csv','w') as file:
			for l, t in self.iterator():
				file.write('{}, {}\n'.format(l, t))
				print(l + '>' + t)
		self.close()

	def iter_locs_kunskapsprov(self):
		# Wait for page to load
		WebDriverWait(self, timeout=10).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'form-control')) == 7)
		# Select test type
		fields = self.find_elements(By.CLASS_NAME, 'form-control')
		select = Select(fields[1])
		select.select_by_value('3')
		# Select language
		select = Select(fields[4])
		#print(select.text)
		select.select_by_value(LANGUAGE[self.config.language])
		for loc in self.config.loc:
			# Select location
			fields[2].clear()
			fields[2].send_keys(loc)
			#fields[2].click()
			dd = self.find_elements(By.TAG_NAME, 'li')
			clicked  = False
			while not clicked:
				try:
					dd[6].click()
				except:
					fields[2].click()
				else:
					clicked = True
			# Wait for results to load
			WebDriverWait(self, timeout=0.01).until(Crawler.__page_load)
			if len(self.find_elements(By.TAG_NAME, 'strong')) > 0:
				yield loc, self.find_elements(By.TAG_NAME, 'strong')[0].text
			else:
				yield loc, ''

	def iter_locs_korprov(self):
		# Wait for page to load
		WebDriverWait(self, timeout=10).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'form-control')) == 7)
		# Select test type
		fields = self.find_elements(By.CLASS_NAME, 'form-control')
		select = Select(fields[1])
		select.select_by_value('12')
		# Select car type
		select = Select(fields[5])
		select.select_by_value(CAR_TYPE[self.config.bil_type])
		for loc in self.config.loc:
			# Select location
			fields[2].clear()
			fields[2].send_keys(loc)
			#fields[2].click()
			dd = self.find_elements(By.TAG_NAME, 'li')
			clicked  = False
			while not clicked:
				try:
					dd[6].click()
				except:
					fields[2].click()
				else:
					clicked = True
			# Wait for results to load
			WebDriverWait(self, timeout=0.01).until(Crawler.__page_load)
			if len(self.find_elements(By.TAG_NAME, 'strong')) > 0:
				yield loc, self.find_elements(By.TAG_NAME, 'strong')[0].text
			else:
				yield loc, ''

	@staticmethod
	def __page_load(d):
		if (len(d.find_elements(By.TAG_NAME, 'strong')) > 0) \
		or (d.find_element(By.XPATH, "//*[contains(text(),'Hittar inga lediga tider som matchar dina val.')]").is_displayed()):
			return True
		return []
