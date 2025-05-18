# Web Scraping Tasks

This repository contains solutions to the following web scraping tasks using Python, Selenium, BeautifulSoup, and other libraries:

- Scrape Product Details like Categories, Price, Ratings and Product URL from Amazon.
- Scrape Tourist Attractions using OpenStreetMap's Overpass API.
- Scrape Gym Data from MagicPin.

## Tech Stack

- Programming Language: Used Python for all tasks.
- BeautifulSoup: Web scraping library for parsing HTML.
- Selenium: Used for dynamic content scraping and interaction with websites that rely on JavaScript.
- Requests: HTTP library to fetch raw HTML content for static websites.
- Overpass API: Used to query tourist attractions from OpenStreetMap.

## Getting Started

### Prerequisites:

1) Install required Python libraries:
   ```bash 
    pip install selenium beautifulsoup4 pandas requests
   ```
   
2) For Amazon Task:

- Install Selenium WebDriver for Chrome/Firefox:
  * Download ChromeDriver [here](https://developer.chrome.com/docs/chromedriver/downloads)
  * Or FirefoxDriver (GeckoDriver) [here](https://github.com/mozilla/geckodriver/releases/tag/v0.36.0)
- Make sure the driver is added to your system's PATH, or specify the full path in the script.

3) To run the scripts, execute `main.py` for the specific task. The resulting CSV file will be saved as `scraped_data.csv`.
