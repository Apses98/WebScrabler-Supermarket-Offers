# Swedish Offers Scraper

This repository contains Python scripts that scrapes product offers from several websites. 
The script utilizes Selenium for web automation and BeautifulSoup for HTML parsing. 
The scraped data is then saved as a JSON file.

### Prerequisites

First time running the script, it will check to ensure that you have the required Python libraries installed. 

### Getting Started

Follow these steps to get started:

+ Clone the repository

+ Run the command: ./run.sh

### Notes

The script uses the Chrome web browser for automation. Make sure you have the ChromeDriver executable in your system's PATH or update the webdriver.Chrome() line in the script with the correct path to the ChromeDriver executable.

If you encounter any missing library issues during execution, the script provides an option to install the required libraries at the very beginning.

The scraped data includes product title, brand, price, unit, and image URL (Stored in json format).

Feel free to contribute to this project by opening issues or submitting pull requests.
