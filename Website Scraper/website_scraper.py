from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import os

def txt_to_csv(txt_file, csv_file):
    with open(txt_file, 'r') as txt_file:
        with open(csv_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for line in txt_file:
                writer.writerow([line.strip()])

# Ask the user for the search query
user_search = input("Enter the website to audit: ")

# Initialize Chrome driver
driver = webdriver.Chrome()

# Open Google homepage
driver.get(user_search)

# Wait for the page to load
#time.sleep(3)

# Parse the HTML content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find elements with <loc> tags in the search results
loc_tags = soup.find_all("loc")

# Extract and write the URLs to a text file
with open("scrape_google_searches.txt", "w", encoding="utf-8") as textfile:
    for loc_tag in loc_tags:
        url = loc_tag.text.strip()
        textfile.write(url + "\n")

# Convert text file to CSV
txt_file = "scrape_google_searches.txt"
csv_file = "scrape_google_searches.csv"
txt_to_csv(txt_file, csv_file)

# Delete the text file
os.unlink(txt_file)

print("The CSV file has been created\n")
driver.quit()



