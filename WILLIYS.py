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

# Function to check if the load more button is present
def is_button_present():
	try:
		button = driver.find_element(*show_more_button_locator)
		#print('button is present')
		return True
	except NoSuchElementException:
		#print('button is not present')
		return False
		
def remove_blocking_element():
	global click_intercepted
	global error_message
	time.sleep(2)
	if click_intercepted:
		try:
			#print("remove blocking element function init")
			pattern = r'data-testid="([^"]+)"'
			matches = re.findall(pattern, error_message)
			#print(matches)
			if len(matches) >= 2:
				match = matches[1]
			else: 
				match = matches[0]

			# Check if a match is found
			if match:
				#print(f"match selected {match}")
				data_test_id = match
				#print(f"data-testid: {data_test_id}")
				blocking_element = driver.find_element(By.XPATH, f"//div[@data-testid='{data_test_id}']")
				element_blocked = True
			else:
				#print("No data-testid found in the error message.\nTrying to get element by class")
				pattern = r'class="([^"]+)"'
				matches = re.findall(pattern, error_message)
				#print(matches)
				if len(matches) >= 2:
					match = matches[1]
				else: 
					match = matches[0]
				# Check if a match is found
				if match:
					#print(f"match selected {match}")
					element_class = match
					#print(f"class: {element_class}")
					blocking_element = driver.find_element(By.XPATH, f"//div[@data-testid='{element_class}']")
					element_blocked = True
				else:
					#print("No class found in the error message.")
					element_blocked = False

		except (NoSuchElementException) as e:
			#print('The button is not blocked by any other element')
			element_blocked = False 
		if element_blocked:
			#print('Another element is blocking the button, trying to remove it!')
			try:
				# Use JavaScript to remove the blocking element from the DOM
				driver.execute_script("arguments[0].remove();", blocking_element)
				#print("Blocking element removed using JavaScript")
				#blocking_element.click()
			except (Exception) as e:
				pass
		click_intercepted = False
	else:
		print("No blocking element present!")

def click_loadMore_button():
	global click_intercepted
	global error_message
	
	#print('Trying to press the load more button.')
	try:
		# Wait for the button to be clickable and click it
		#print('Locating the load more button.')
		button = wait.until(EC.element_to_be_clickable(show_more_button_locator))
		time.sleep(1)
		#print('Scrolling to the bottom of the page.')
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
		#print('Clicking the button.')
		button.click()
		time.sleep(1)
	except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
		# Handle Exception
		print('Error!! \n')
		#print(e)
		
	except (ElementClickInterceptedException) as e:
		pattern = r'intercepted'
		match = re.search(pattern, str(e))
		if match:
			#print("an element is blocking the click")
			error_message = str(e)
			click_intercepted = True
		else:
			click_intercepted = False	
			
			
click_intercepted = False
error_message = ""

		
# URL of your willys page
url = 'https://www.willys.se/erbjudanden/ehandel'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode 
driver = webdriver.Chrome(options=chrome_options)
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
	
	show_more_button_locator = (By.XPATH, "//button[@data-testid='load-more-btn']")
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
		#print(f"Error pressing the cookies reject button.\n{e}")
		pass
	except (ElementClickInterceptedException) as e:
		pattern = r'intercepted'
		match = re.search(pattern, str(e))
		if match:
			#print("an element is blocking the click")
			error_message = str(e)
			click_intercepted = True
		else:
			click_intercepted = False
		pass
		
	if click_intercepted:
		#print("click intercepted, trying to remove")
		remove_blocking_element()
	
	#print("Trying to click the load more button")
	click_loadMore_button()

	if click_intercepted:
		#print("click intercepted, trying to remove")
		remove_blocking_element()
		
	# Scroll until the button disappears
	while is_button_present():
		try:
			#print('Scrolling to the bottom')
			# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")	
			try:
				load_more_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='load-more-btn']")))
			except (Exception) as e:
				pass
			driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });", load_more_button)
			time.sleep(1)
		except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
			# print(e)
			#print('the button is not present, breaking the loop')
			break	
		except (ElementClickInterceptedException) as e:	
			pattern = r'intercepted'
			match = re.search(pattern, str(e))
			if match:
				#print("an element is blocking the click")
				error_message = str(e)
				click_intercepted = True
			else:
				click_intercepted = False
			
		if click_intercepted:
			#print("click intercepted, trying to remove")
			remove_blocking_element()
	
	# Trying to click the button one last time, to make sure it is not present
	try:
		#print('Waiting to locat the button!')
		button = wait.until(EC.element_to_be_clickable(show_more_button_locator))
		#print('Trying to press the button')
		button.click()
		time.sleep(1)
	except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
		#print('Success, the button was not present.\n')
		pass


	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	html_content = driver.page_source
	soup = BeautifulSoup(html_content, 'html.parser')


	# Find offers
	offer_cards = soup.find_all('div', class_='sc-dfc0c17a-0 bEmoOU')
	
	offers_data = []
	
	info_block =	{
			"StoreName": "Williys",
			"TimeDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
			"StoreUrl": url
			}
	offers_data.append(info_block)
	
	for card in offer_cards:
		
		# product title / name
		title_element = card.find('div', class_='sc-dfc0c17a-6 iqMNoN')

		# product brand
		brand_element = card.find('div', class_='sc-dfc0c17a-7 iVRgmk')
		
		# price in kr
		price_element1 = card.find('span', class_='sc-9270b5eb-2 fVzqtS')
        
		# price in pennies (öre)
		price_element2 = card.find('span', class_='sc-9270b5eb-5 czApoH')
        
		# prefix
		quantity_element = card.find('div', class_='sc-dfc0c17a-13 kDhKOX')        
        
		# suffix
		unit_element = card.find('span', class_='sc-9270b5eb-6 eKiAfO')
        
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
		image_url = image_element["src"] if image_element else ""
		
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
		
	print('Creating JSON file')
	# Write the data as jason to file 
	if len(sys.argv) > 1:
		path = sys.argv[1] + '/WILLIYS.json'
	else:
		path = 'WILLIYS.json'
	with open(path, 'w') as json_file:
		json.dump(offers_data, json_file, indent=2, ensure_ascii=False)
		
	print(f"Data saved successfully to {path} file")
	
#print('Driver is exiting')
driver.quit()
