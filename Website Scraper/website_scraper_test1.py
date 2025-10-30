from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

# Ask the user for the search query
user_search = input("Enter the website to audit: ")
search_query = "site:" + user_search

# Initialize Chrome driver
driver = webdriver.Chrome()

# Open Google homepage
driver.get("https://www.google.com/")

# Find the search input field and enter the query
search_input = driver.find_element(By.NAME, "q")
search_input.send_keys(search_query)
search_input.send_keys(Keys.RETURN)

try:
    # Wait for the search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g")))

    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find elements for search names and descriptions
    search_results = soup.select("div.g")
    
    # Print the collected data
    print("The CSV file has been created\n")

    with open("scrape_google_searches.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Site Name", "Site Description"])

        # Loop through all search results and write them to CSV
        for result in search_results:
            search_name = result.select_one("cite").get_text()
            search_description = result.select_one("div.IsZvec").get_text()
            writer.writerow([search_name, search_description])

finally:
    # Close the Chrome driver
    driver.quit()
