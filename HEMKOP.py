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

		
# URL of your Hemköp page
url = 'https://www.hemkop.se/erbjudanden'

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
	print("Timed out waiting for page to load")

time.sleep(10)

wait = WebDriverWait(driver, 5)

if status:
	# Get the HTML content after the page has loaded
	html_content = driver.page_source
	
	cookies_message_reject_button_locator = (By.ID, 'onetrust-reject-all-handler')
	

	try:
		#print('Trying to press the reject cookies button.')
		time.sleep(1)
		wait.until(EC.element_to_be_clickable(cookies_message_reject_button_locator))
		
		# Find the cookies reject button element
		cookies_reject_button = driver.find_element(*cookies_message_reject_button_locator)
		cookies_reject_button.click()
		click_intercepted = False
	except (Exception) as e:
		print("Error pressing the cookies reject button.\n")
		pass
	except (ElementClickInterceptedException) as e:
		pattern = r'intercepted'
		match = re.search(pattern, str(e))
		if match:
			print("an element is blocking the click")
		pass

	
	# Scroll until all offers are loaded // Scroll to the bottom 20 times
	for i in range(20):
		#print('Scrolling to the bottom')
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")	
		time.sleep(2)
		
	html_content = driver.page_source
	soup = BeautifulSoup(html_content, 'html.parser')


	# Find offers
	offer_cards = soup.find_all('div', class_='sc-878cc7d7-0 jlkWRE')
	
	offers_data = []
	
	info_block = {
			"StoreName": "Hemköp",
			"TimeDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
			"StoreUrl": url
			}
	offers_data.append(info_block)
	
	for card in offer_cards:
		
		# product title / name
		title_element = card.find('div', class_='sc-d95e8214-6 kRuShj')

		# product brand
		brand_element = card.find('div', class_='sc-fdd75863-4 caoSJr')
		
		# prefix ( might include price for wight products )
		quantity_element = card.find('span', class_='sc-c05686a6-7 eeOXTA')
		
		# Offer Price Element 1
		price_element1 = card.find('span', attrs={'data-testid': 'price'})
        
		# Offer Price Element 2
		price_element2 = card.find('span', class_='sc-9270b5eb-5 czApoH')
        
		# suffix
		unit_element = card.find('span', attrs={'data-testid': 'price-unit'})
        
		# image url
		image_element = card.find('img')
        
		# Extract information if elements exist
		title = title_element.get_text(strip=True) if title_element else ""
		brand = brand_element.get_text(strip=True) if brand_element else ""
		price = price_element1.get_text(strip=True) if price_element1 else ""
		price2 = price_element2.get_text(strip=True) if price_element2 else ""
		unit = unit_element.get_text(strip=True) if unit_element else ""
		quantity = quantity_element.get_text(strip=True) if quantity_element else ""
		
		image_url = image_element["src"] if image_element else ""
		
		'''  
		#debugg
		print(f"Title: {title}")
		print(f"Brand: {brand}")
		print(f"Price: {quantity} {price} {price2} {unit}")
		print(f"image link: {image_url}")
		print("-" * 30)
		'''
		
		offer_data = {
			"Title": title,
			"Brand": brand, 
			"Price": f"{quantity} {price} {price2} {unit}", 
			"Image_URL": image_url
		}
		
		offers_data.append(offer_data)
		
	#print('Creating JSON file')
	# Write the data as jason to file 
	if len(sys.argv) > 1:
		path = sys.argv[1] + '/HEMKOP.json'
	else:
		path = 'HEMKOP.json'
	with open(path, 'w') as json_file:
		json.dump(offers_data, json_file, indent=2, ensure_ascii=False)
		
	print(f"Data saved successfully to {path} file")
	
#print('Driver is exiting')
driver.quit()
