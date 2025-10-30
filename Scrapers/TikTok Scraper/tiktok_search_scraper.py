from bs4 import BeautifulSoup
from selenium import webdriver
import csv

# Ask the user for the TikTok profile URL
tiktok_search = input("Enter the category you would like to search:")

tiktok_url = f"https://www.tiktok.com/search/user?q={tiktok_search}&t=1713128112637"

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

        # Find elements for posts, likes, comments, and saved
        user_names = soup.find_all("p", attrs={"data-e2e": "search-user-unique-id"})
        handle_names = soup.find_all("p", attrs={"data-e2e": "search-user-nickname"})
        followers = soup.find_all("span", attrs={"data-e2e": "search-follow-count"})

        # Print the collected data
        print("The CSV file has been created")

        # Write data to CSV
        with open("scrape_search_tiktok.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Username", "@ Handle", "Followers"])
            writer.writerow(["", "", ""])

            # Loop through all data and write them to CSV
            for user_name, handle_name, follower in zip(user_names, handle_names, followers):
                user_name_text = user_name.text.strip()
                handle_name_text = handle_name.text.strip()
                follower_text = follower.text.strip()
                writer.writerow([user_name_text, handle_name_text, follower_text])

        # Close the Chrome driver after scraping
        driver.quit()
        break

    else:
        print("Please wait until the page fully loads.")
