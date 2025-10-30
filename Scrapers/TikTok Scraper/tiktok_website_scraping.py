from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

# Ask the user for the TikTok profile URL
tiktok_url = input("Enter the TikTok profile URL: ")

# Initialize Chrome driver (you need to have chromedriver installed and in your PATH)
driver = webdriver.Chrome()

# Open the TikTok profile page
driver.get(tiktok_url)


while True:
    
    # Sleep until user enters 'Y'
    user_input = input("Enter 'Y' when the page has fully loaded: ").strip().upper()
    if user_input == 'Y' or user_input == 'y':

        # Parse the HTML content
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find elements for posts, likes, comments, and saved
        acc_name = soup.find("h1", attrs={"data-e2e": "user-title"}).text
        acc_desc = soup.find("h2", attrs={"data-e2e": "user-bio"}).text
        following = soup.find("strong", attrs={"data-e2e": "following-count"}).text
        followers = soup.find("strong", attrs={"data-e2e": "followers-count"}).text
        likes = soup.find("strong", attrs={"data-e2e": "likes-count"}).text

        # Close the Chrome driver
        driver.quit()

        # Print the collected data
        print("The CSV file has been created")
        print("")

        with open("scrape_tiktok_website.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account Name", "Bio", "Following", "Followers", "Likes"])
            writer.writerow([acc_name, acc_desc, following, followers, likes])

        break

    else:
        print("Please wait until the page fully loads.")

