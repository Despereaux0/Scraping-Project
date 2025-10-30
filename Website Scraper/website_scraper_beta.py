from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from bs4 import BeautifulSoup
import csv
import time

# Find and click the "More results" button
def click_more_results():
    more_results_button = driver.find_element(By.XPATH, "//span[text()='More results']")
    more_results_button.click()

# Scroll to the bottom of the page
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

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

user_input = input("Enter 'Y' or 'y' once the page has loaded : ")
if user_input.lower() == 'y':
    # Main loop to keep scrolling and clicking the "More results" button
    for _ in range(6):
        scroll_to_bottom()
        time.sleep(2)

    site_names_set = set()  # To store unique site names
    while True:
        try:
            scroll_to_bottom()
            time.sleep(2)
            click_more_results()
        except ElementNotInteractableException:
            break
    
    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find elements for site names in the search results
    search_names = soup.find_all("cite", class_="qLRx3b tjvcx GvPZzd cHaqb")

    # Collect unique site names
    for search_name in search_names:
        site_name = search_name.get_text(strip=True).replace("›", "/").strip()
        if site_name.endswith("...") or site_name.endswith("/"):
            continue
        site_names_set.add(site_name)
        
    # Sort the site names alphabetically
    sorted_site_names = sorted(site_names_set)
    
    # Write the sorted site names to a CSV file
    with open("scrape_google_searches.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Site Name"])
        for site_name in sorted_site_names:
            writer.writerow([site_name])

    print("The CSV file has been created\n")
    driver.quit()

else:
    print("Please wait for the page to load")
