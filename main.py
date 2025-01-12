import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.chrome.options import Options

# Configure Selenium for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize Selenium WebDriver
driver = webdriver.Chrome(options=chrome_options)  # Headless Chrome setup

# CSV File to Store Data
csv_file = "waitlist_length_data.csv"

# Function to save data
def save_to_csv(data, filename):
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Write header if file is empty
            writer.writerow(["Timestamp", "Total Parties"])
        writer.writerow(data)

# Function to scrape the current waitlist length
def collect_waitlist_data():
    try:
        print("Step 1: Open URL")
        # Open the waitlist page
        url = "https://gosnappy.io/lineup/?storeId=9371&lang=en&noSms=false&force=false"
        driver.get(url)

        print("Step 2: Wait for the number of parties in line")
        # Locate the element showing the total parties in line
        parties_in_line_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "linesize"))
        )
        parties_in_line_text = parties_in_line_element.text.strip()

        # Extract the number of parties from the text
        parties_in_line = int(re.search(r"\d+", parties_in_line_text).group())
        print(f"Total parties in line: {parties_in_line}")

        # Log the data
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        save_to_csv([timestamp, parties_in_line], csv_file)

    except Exception as e:
        print(f"Error: {e}")

# Main Script
if __name__ == "__main__":
    try:
        # Collect data periodically
        while True:
            collect_waitlist_data()
            print("Waiting for the next collection interval...")
            time.sleep(300)  # Collect data every 5 minutes
    finally:
        # Close the browser
        driver.quit()