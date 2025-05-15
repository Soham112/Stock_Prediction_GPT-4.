# image_trading_view.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os

# Set up Chrome options to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

# Path to the ChromeDriver executable
chrome_driver_path = 'C:\\Users\\Soham\\Downloads\\chromedriver-win64\\chromedriver.exe'  # Ensure this path matches your setup

# Initialize the Service with the ChromeDriver path
service = Service(chrome_driver_path)

def capture_chart_screenshot(stock_symbol):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = f"https://www.tradingview.com/chart/?symbol={stock_symbol}"
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    screenshot_path = f"../images/{stock_symbol}.png"
    driver.save_screenshot(screenshot_path)
    driver.quit()
    return screenshot_path

def extract_images():
    # List of stock symbols to capture
    stocks = ['RELIANCE', 'TCS', 'HINDUNILVR']  # Add more stock symbols as needed

    # Ensure the screenshots directory exists
    os.makedirs('../images', exist_ok=True)

    for stock in stocks:
        try:
            capture_chart_screenshot(stock)
            print(f"Screenshot captured for {stock}")
        except Exception as e:
            print(f"Failed to capture screenshot for {stock}: {e}")
