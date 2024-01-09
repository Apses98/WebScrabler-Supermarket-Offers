import subprocess
import sys

def check_libraries():
	libraries = [
		'json',
		'requests',
		'time',
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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

# Put URL of your prefered ICA store here
# Make sure you pick the "erbjudanden" webpage
url = 'https://www.ica.se/erbjudanden/maxi-ica-stormarknad-karlstad-1004029/'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode 

driver = webdriver.Chrome(options=chrome_options)
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

time.sleep(2)

# Get the HTML content after the page has loaded
html_content = driver.page_source

# Close the browser
driver.quit()

if status:
	soup = BeautifulSoup(html_content, 'html.parser')
	
	# Find offers 
	offer_cards = soup.find_all('article', class_='offer-card')

	offers_data = []

	info_block =	{
			"StoreName": "ICA",
			"TimeDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
			"StoreUrl": url
			}
	offers_data.append(info_block)
	
	for card in offer_cards:
		title = card.find('p', class_='offer-card__title').get_text(strip=True)
		brand = card['data-promotion-brand']

		# Check if the elements exist before accessing their properties
		price_element = card.find('span', class_='firstValue')
		quantity_element = card.find('div', class_='prefix')        
		unit_element = card.find('div', class_='suffix')
		promotion_container = card.find('span', class_='priceSplashContainer')
		image_element = card.find('img', class_='offer-card__image-inner')
        
		# Check if the promotion container exists before accessing its properties
		if promotion_container:
			promotion_element = promotion_container.find('span', class_='sr-only')
		else:
			promotion_element = None  # or any default value you prefer

		# Extract information if elements exist
		price = price_element.get_text(strip=True) if price_element else ""
		unit = unit_element.get_text(strip=True) if unit_element else ""
		promotion = promotion_element.get_text(strip=True) if promotion_element else ""
		quantity = quantity_element.get_text(strip=True) if quantity_element else ""
		image_url = image_element["src"] if image_element else ""
        

		'''
		#debugg
		print(f"Title: {title}")
		print(f"Brand: {brand}")
		print(f"Price: {quantity} {price}{unit}")
		print(f"image link: {image_url}")
		print(f"Promotion: {promotion}")
		print("-" * 30)
		'''
		
		# Create a dictionary for each offer
		offer_data = {
			"Title": title,
			"Brand": brand, 
			"Price": f"{quantity} {price}{unit}", 
			"Image_URL": image_url
		}
        
		offers_data.append(offer_data)
        
        if len(sys.argv) > 1:
		path = sys.argv[1] + '/ICA_offers.json'
	else:
		path = 'ICA_offers.json'
	# Write the data as jason to file 
	with open(path, 'w') as json_file:
		json.dump(offers_data, json_file, indent=2, ensure_ascii=False)
            
	#debugg
	print("Data saved successfully to ICA_offers.json file")

else:
	print("Error: Failed to retrieve the webpage.")

