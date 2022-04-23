from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import configparser
import os
import sys

class Crawler(webdriver.Chrome):
	def __init__(self, pn, locs, test_type, bil_type):
		service = Service('./chromedriver')
		super().__init__(service=service)
		self.get("https://fp.trafikverket.se/Boka/#/")
		self.implicitly_wait(10)
		self.pn = pn
		self.locs = []
		if len(locs):
			self.locs = locs
		else:
			if test_type == 'Korprov':
				with open('korprov-locs.txt','r') as file:
					for loc in file.readlines():
						self.locs.append(loc.strip())
			else:
				with open('kunskaps-locs.txt','r') as file:
					for loc in file.readlines():
						self.locs.append(loc.strip())
		if test_type == 'Korprov':
			self.iterator = self.iter_locs_korprov
		else:
			self.iterator = self.iter_locs_kunskapsprov

	def navigate_no_login(self):
		# Click 'Boka' button
		buttons = self.find_elements(By.CLASS_NAME, 'col-sm-3')
		buttons[0].click()
		self.implicitly_wait(10)
		# Select book without login
		opts = self.find_elements(By.CLASS_NAME,'list-group-item')
		opts[3].click()
		self.implicitly_wait(10)
		# Click 'Continue'
		cont = self.find_elements(By.CLASS_NAME, 'col-sm-4.col-sm-offset-3.col-sm-push-2')
		cont[0].click()
		self.implicitly_wait(10)
		# Input personnummer
		ssn = self.find_element(By.ID, 'social-security-number-input')
		ssn.send_keys(self.pn)
		# Select B
		opts = self.find_elements(By.CLASS_NAME,'list-group-item')
		opts[3].click()
		# Wait for page to load
		# WebDriverWait(self, timeout=3).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'form-control')) == 7)
		with open('korprov-times.csv','w') as file:
			for l, t in self.iterator():
				file.write('{}, {}\n'.format(l, t))
				print(l + '>' + t)
		self.close()

	def navigate_with_login(self):
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
			for l, t in self.iter_locs_kunskapsprov():
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
		select.select_by_value('4')
		for loc in self.locs:
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
		select.select_by_value('4')
		for loc in self.locs:
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
