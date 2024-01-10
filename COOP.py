import subprocess


def check_libraries():
	libraries = [
		'json',
		'requests',
		'time',
		're',
		'sys',
		'bs4',
		'selenium',
		'datetime',
	]

	missing_libraries = []

	for lib in libraries:
		try:
			__import__(lib)
		except ImportError:
			if lib == 'bs4':
				missing_libraries.append('beautifulsoup4')
			else:
				missing_libraries.append(lib)


	if missing_libraries:
		print("The following libraries are missing:")
		for missing_lib in missing_libraries:
			print(f" - {missing_lib}")
			install_libraries = input("Do you want to install these missing libraries? (y/n): ").lower()
			if install_libraries == 'y':
				for missing_lib in missing_libraries:
					subprocess.run(['pip', 'install', missing_lib])
				print("Libraries installed successfully.")
				return True
			else:
				print("Exiting without installing missing libraries.")
				return False
	else:
		print("All required libraries are available.")
		return True

  
    
    
    


# Check if libraries are available
if check_libraries():
	# Continue with the rest of your code
	print("Proceeding with the script...")
else:
	print("Exiting due to missing libraries.")
	sys.exit(1)
	
import json
import requests
import time
import re
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException, TimeoutException
from datetime import datetime

def convert_to_int(text):
	result = ''
	for ch in text:
		if ch == '1' or ch == '2' or ch == '3' or ch == '4' or ch == '5' or ch == '6' or ch == '7' or ch == '8' or ch == '9' or ch == '0':
			result += ch
	try:
		int_result = int(result)
	except (Exception) as e:
		int_result = 0
	
	return int_result
		

def reject_cookies(locator):
	try:
		#print('Trying to press the reject cookies button.')
		time.sleep(1)
		wait.until(EC.element_to_be_clickable(locator))

		# Find the cookies reject button element
		cookies_reject_button = driver.find_element(*locator)
		cookies_reject_button.click()
	except (Exception) as e:
		#print(f"Error pressing the cookies reject button.")
		pass
		
# URL of your willys page
url = 'https://www.coop.se/handla/aktuella-erbjudanden/'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode 
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
driver.get(url)

# Wait for the page to load
timeout = 10
try:
	element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
	WebDriverWait(driver, timeout).until(element_present)
	status = True
except TimeoutException:
	status = False
	#print("Timed out waiting for page to load")

time.sleep(10)

wait = WebDriverWait(driver, 5)

if status:
	# Get the HTML content after the page has loaded
	html_content = driver.page_source
	soup = BeautifulSoup(html_content, 'html.parser')
	
	cookies_message_reject_button_locator = (By.ID, 'cmpwelcomebtnno')
	
	reject_cookies(cookies_message_reject_button_locator)
		
	
	
	
	offer_pages = soup.find_all('a', class_='Pagination-page u-outlineSolidBase2 u-marginHxxxsm u-md-paddingAsm u-xsm-paddingAxsm')
	
	number_of_pages = convert_to_int(offer_pages[len(offer_pages) - 1].get_text(strip=True))
		
	
	offers_data = []
	
	info_block =	{
			"StoreName": "COOP",
			"TimeDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
			"StoreUrl": url
			}
			
	offers_data.append(info_block)
	
	# get offers on every offer page!
	for i in range(0, number_of_pages):
		if i != 0 :
			url = f'https://www.coop.se/handla/aktuella-erbjudanden/?page={ i + 1 }'
		driver.get(url)

		# Wait for the page to load
		timeout = 10
		try:
			element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
			WebDriverWait(driver, timeout).until(element_present)
			status = True
		except TimeoutException:
			status = False
			#print("Timed out waiting for page to load")
	
		reject_cookies(cookies_message_reject_button_locator)
		
		if status:
			# Get the HTML content after the page has loaded
			html_content = driver.page_source
			soup = BeautifulSoup(html_content, 'html.parser')
		else:
			print('Error loading the page!')
			print('exiting')
			sys.exit(1)
	
		# Find offers
		offer_cards = soup.find_all('article', class_='ProductTeaser ProductTeaser--clickable')
	
	
		for card in offer_cards:
			
			# product title / name
			title_element = card.find('h3', class_='ProductTeaser-heading')

			# product brand
			brand_element = card.find('div', class_='ProductTeaser-brand')
			
			# price in kr
			price_element1 = card.find('span', class_='Splash-priceLarge')
			
			# price in pennies (öre)
			price_element2 = card.find('span', class_='Splash-priceSup')
			
			# suffix
			unit_element = card.find('span', class_='Splash-priceSub')
			# prefix
			quantity_element = card.find('span', class_='Splash-pricePre')        
			
			# image url
			image_element = card.find('img')
		
			# Extract information if elements exist
			title = title_element.get_text(strip=True) if title_element else ""
			brand = brand_element.get_text(strip=True) if brand_element else ""
			price = price_element1.get_text(strip=True) if price_element1 else ""
			price2 = price_element2.get_text(strip=True) if price_element2 else ""
			price = price + ' ' + price2
			unit = unit_element.get_text(strip=True) if unit_element else ""
			quantity = quantity_element.get_text(strip=True) if quantity_element else ""
			try:
				image_url = image_element["src"] if image_element else ""
			except (Exception) as e:
				image_url = ""
				pass
			'''
			#debugg
			print(f"Title: {title}")
			print(f"Brand: {brand}")
			print(f"Price: {quantity} {price}{unit}")
			print(f"image link: {image_url}")
			print("-" * 30)
			'''
			
			offer_data = {
				"Title": title,
				"Brand": brand, 
				"Price": f"{quantity} {price}{unit}", 
				"Image_URL": image_url
			}
			
			offers_data.append(offer_data)
			time.sleep(1)
			
	#print('Creating JSON file')
	# Write the data as jason to file 
	if len(sys.argv) > 1:
		path = sys.argv[1] + '/COOP.json'
	else:
		path = 'COOP.json'
	with open(path, 'w') as json_file:
		json.dump(offers_data, json_file, indent=2, ensure_ascii=False)
		
	print(f"Data saved successfully to {path} file")
	
#print('Driver is exiting')
driver.quit()
