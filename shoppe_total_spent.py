from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

# Ask the user for the TikTok profile URL
tiktok_url = input("Enter the URL: ")

# Initialize Chrome driver (you need to have chromedriver installed and in your PATH)
driver = webdriver.Chrome()

# Open the TikTok profile page
driver.get(tiktok_url)

while True:
    # Sleep until user enters 'Y'
    user_input = input("Enter 'Y' when the page has fully loaded: ").strip().upper()
    if user_input == 'Y':

        # Parse the HTML content
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find elements with class "t7TQaf" for Order Total
        order_totals = soup.find_all("div", class_="t7TQaf")
        
        # Find elements with class "bv3eJE" for Completed
        completions = soup.find_all("div", class_="bv3eJE")

        # Close the Chrome driver
        driver.quit()

        # Print the collected data
        print("The CSV file has been created")
        print("")

        # Write the data to a CSV file
        with open("scrape_tiktok.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Order Total", "Status"])

            # Loop through all order totals and completions and write them to CSV
            for order_total, completion in zip(order_totals, completions):
                order_total_text = order_total.text.strip().replace("RM", "")
                completion_text = completion.text.strip()
                writer.writerow([order_total_text, completion_text])

        break
    else:
        print("Please wait until the page fully loads.")
