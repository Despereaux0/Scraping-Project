from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

# Ask the user for the TikTok profile URL
instagram_url = input("Enter the Instagram post URL: ")

# Initialize Chrome driver (you need to have chromedriver installed and in your PATH)
driver = webdriver.Chrome()

# Open the TikTok profile page
driver.get(instagram_url)


while True:
    
    # Sleep until user enters 'Y'
    user_input = input("Enter 'Y' when the page has fully loaded: ").strip().upper()
    if user_input == 'Y' or user_input == 'y':

        # Parse the HTML content
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find elements for posts, likes, comments, and saved
        likes = soup.find("span", attrs={"class": "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"}).text
        commentor_names = soup.find_all("div", attrs={"class": "x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xw3qccf x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"})
        comments_texts = soup.find_all("span", attrs={"class": "_ap3a _aaco _aacu _aacx _aad7 _aade"})

        # Close the Chrome driver
        driver.quit()

        # Print the collected data
        print("The CSV file has been created")
        print("")

        with open("scrape_instagram.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Number of Likes", "Commentor Name", "Comment"])
            writer.writerow([likes])

            # Loop through all comments and write them to CSV
            for commentor_name, comment_text in zip(commentor_names, comments_texts):
                commentor_name_text = commentor_name.text.strip()
                comment_text_text = comment_text.text.strip()
                writer.writerow(["", commentor_name_text, comment_text_text])

        break

    else:
        print("Please wait until the page fully loads.")

