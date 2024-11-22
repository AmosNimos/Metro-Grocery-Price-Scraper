from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re

# Setup headless Firefox
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

def extract_price(price_text):
    """ Extract the first numeric value from a string. """
    if not price_text:
        return None
    # Clean the text and extract the first floating-point number
    match = re.search(r'\d+(\.\d+)?', price_text.replace(',', ''))
    if match:
        return float(match.group())
    return None

try:
    # Load the webpage
    url = "https://www.metro.ca/en/online-grocery/search?filter=Ground"
    driver.get(url)
    driver.implicitly_wait(10)  # Allow time for JavaScript to load

    # Parse the page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all product tiles with discounts
    products = soup.find_all('div', class_='default-product-tile tile-product item-addToCart tile-product--effective-date')

    for product in products:
        # Find product name
        title_tag = product.find('div', class_='head__title')
        product_name = title_tag.get_text(strip=True) if title_tag else 'Unknown Product'
        print(f"\nProduct: {product_name}")

        # Find regular price (skip 'invisible-text')
        regular_price_tag = product.find('div', class_='pricing__before-price')
        regular_price_text = regular_price_tag.get_text(strip=True) if regular_price_tag else None
        regular_price = extract_price(regular_price_text)

        # Find promo price
        promo_price_tag = product.find('div', class_='pricing__secondary-price promo-price')
        promo_price_text = promo_price_tag.get_text(strip=True).split('/')[0] if promo_price_tag else None
        current_price = extract_price(promo_price_text)

        # Ensure both prices are available
        if regular_price and current_price:
            discount = regular_price - current_price
            print(f"Regular Price: ${regular_price:.2f}")
            print(f"Current Price: ${current_price:.2f}")
            print(f"Discount: ${discount:.2f}")
        else:
            print("Price extraction failed or data missing.")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()
