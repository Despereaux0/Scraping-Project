from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv

# Function to get the depth of a URL
def get_url_depth(url):
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/')
    return path.count('/')

# Function to sort URLs
def sort_urls(urls):
    # Sort the URLs based on custom criteria
    sorted_urls = sorted(urls, key=lambda x: (x.startswith("https://www.holamascot.com/product"), get_url_depth(x), x))
    return sorted_urls

# Function to delete odd-numbered lines from a list
def delete_odd_lines(data):
    return [data[i] for i in range(len(data)) if i % 2 == 0]

# Read URLs from CSV file
def read_urls_from_csv(file_path):
    urls = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            urls.extend(row)
    return urls

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

while True:
    # Sleep until user enters 'Y'
    user_input = input("Enter 'Y' when the page has fully loaded: ").strip().upper()
    if user_input == 'Y':
        # Parse the HTML content
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find elements for site names only
        search_names = soup.find_all("cite", attrs={"class": "qLRx3b tjvcx GvPZzd cHaqb", "role": "text"})

        # Close the Chrome driver
        driver.quit()

        # Print the collected data
        print("The CSV file has been created")
        print("")

        with open("scrape_google_searches.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Site Name"])

            # Loop through all site names and write them to CSV
            for search_name in search_names:
                search_name_text = search_name.text.strip()
                writer.writerow([search_name_text.replace('›', '/').replace(' ', '')])

        break
    else:
        print("Please wait until the page fully loads.")

# Path to the CSV file
csv_file_path = "scrape_google_searches.csv"

# Read URLs from CSV
urls = read_urls_from_csv(csv_file_path)

# Delete odd-numbered lines
urls = delete_odd_lines(urls)

# Sort the URLs
sorted_urls = sort_urls(urls)

# Write sorted URLs into a new CSV file
output_csv_path = "website_audit.csv"
with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Sorted URLs"])
    writer.writerows([[url] for url in sorted_urls])

print("Sorted URLs have been written to:", output_csv_path)
