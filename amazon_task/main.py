import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Browser setup
options = Options()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")

# Start the browser
driver = webdriver.Chrome(options=options)

# Defining our categories for scraping
categories = [
    {"Category": "Electronics", "Subcategory": "Mobiles", "URL": "https://www.amazon.in/s?k=mobiles"},
    {"Category": "Electronics", "Subcategory": "Laptops", "URL": "https://www.amazon.in/s?k=laptops"},
    {"Category": "Fashion", "Subcategory": "Men's Clothing", "URL": "https://www.amazon.in/s?k=mens+clothing"},
    {"Category": "Fashion", "Subcategory": "Women's Clothing", "URL": "https://www.amazon.in/s?k=womens+clothing"},
    {"Category": "Home", "Subcategory": "Home Decor", "URL": "https://www.amazon.in/s?k=home+decor"},
    {"Category": "Books", "Subcategory": "Fiction", "URL": "https://www.amazon.in/s?k=fiction+books"},
    {"Category": "Beauty", "Subcategory": "Makeup", "URL": "https://www.amazon.in/s?k=makeup"},
    {"Category": "Sports", "Subcategory": "Fitness", "URL": "https://www.amazon.in/s?k=fitness+equipment"},
    {"Category": "Toys", "Subcategory": "Board Games", "URL": "https://www.amazon.in/s?k=board+games"},
    {"Category": "Grocery", "Subcategory": "Snacks", "URL": "https://www.amazon.in/s?k=snacks"}
]

product_data = []

try:
    for cat in categories:
        print(f"\n Scraping {cat['Subcategory']}...")
        driver.get(cat["URL"])

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"]'))
            )
        except:
            print(f"Timeout while waiting for products in {cat['Subcategory']}")
            continue

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        print(f" → Found {len(products)} products")

        count = 0
        for item in products:
            if count >= 10:
                break

            try:
                # Using Amazon's selector
                title_tag = item.select_one("h2 a.a-link-normal")
                if not title_tag:
                    raise ValueError("Missing title or link")

                title = title_tag.get_text(strip=True)
                url = "https://www.amazon.in" + title_tag['href']

                price_tag = item.select_one('.a-price .a-offscreen')
                price = price_tag.text.strip() if price_tag else "N/A"

                rating_tag = item.select_one('.a-icon-alt')
                rating = rating_tag.text.strip() if rating_tag else "N/A"

                print(f"Parsed: {title[:40]} | {price} | {rating}")

                product_data.append({
                    "Category": cat["Category"],
                    "Subcategory": cat["Subcategory"],
                    "Product Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Product URL": url
                })
                count += 1

            except Exception as e:
                print(f"Skipped one item: {e}")
                continue

finally:
    driver.quit()

    if product_data:
        df = pd.DataFrame(product_data)
        df.to_csv("scraped_data.csv", index=False)
        print(f"\n Saved {len(df)} products to 'scraped_data.csv")
    else:
        print("No product data was saved.")
