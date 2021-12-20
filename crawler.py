from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

def get_time(driver, pn, locs):
	# Click 'Boka' button
	buttons = driver.find_elements(By.CLASS_NAME, 'col-sm-3')
	buttons[0].click()
	driver.implicitly_wait(10)
	# Select book without login
	opts = driver.find_elements(By.CLASS_NAME,'list-group-item')
	opts[3].click()
	driver.implicitly_wait(10)
	# Click 'Continue'
	cont = driver.find_elements(By.CLASS_NAME, 'col-sm-4.col-sm-offset-3.col-sm-push-2')
	cont[0].click()
	driver.implicitly_wait(10)
	# Input personnummer
	ssn = driver.find_element(By.ID, 'social-security-number-input')
	ssn.send_keys(pn)
	# Select B
	opts = driver.find_elements(By.CLASS_NAME,'list-group-item')
	opts[3].click()
	# Wait for page to load
	WebDriverWait(driver, timeout=3).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'form-control')) == 7)
	# Select test type
	fields = driver.find_elements(By.CLASS_NAME, 'form-control')
	select = Select(fields[1])
	select.select_by_value('12')
	# Select car type
	select = Select(fields[5])
	select.select_by_value('4')
	for loc in locs:
		#driver.implicitly_wait(10)
		# Select location
		fields[2].clear()
		fields[2].send_keys(loc)
		
		#fields[2].click()
		dd = driver.find_elements(By.TAG_NAME, 'li')
		clicked  = False
		while not clicked:
			try:
				dd[6].click()
			except:
				fields[2].click()
			else:
				clicked = True
		# Wait for results to load
		try:
			WebDriverWait(driver, timeout=0.1).until(lambda d: len(d.find_elements(By.TAG_NAME, 'strong')) > 0)
		except:
			yield loc, '' # Return null if no result'''
		else:
			times = driver.find_elements(By.TAG_NAME, 'strong')
			yield loc, times[0].text


chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service('/Users/vk/dev/korprov/chromedriver')
driver = webdriver.Chrome(service=service)#, options=chrome_options)
driver.get("https://fp.trafikverket.se/Boka/#/")
driver.implicitly_wait(10)
pn = '19890609-1684'
#locs = ['Alingsås', 'Arjeplog', 'Arvidsjaur']
locs = []
with open('korprov-locs.txt','r') as file:
	for loc in file.readlines():
		locs.append(loc.strip())
with open('korprov-times.csv','w') as file:
	for l, t in get_time(driver, pn, locs):
		file.write('{}, {}\n'.format(l, t))
		print(l + '>' + t)
driver.close()