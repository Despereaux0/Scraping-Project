from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

# Ask the user for the TikTok profile URL
facebook_url = input("Enter the FaceBook post URL: ")

# Initialize Chrome driver (you need to have chromedriver installed and in your PATH)
driver = webdriver.Chrome()

# Open the TikTok profile page
driver.get(facebook_url)


while True:
    
    # Sleep until user enters 'Y'
    user_input = input("Enter 'Y' when the page has fully loaded: ").strip().upper()
    if user_input == 'Y' or user_input == 'y':

        # Parse the HTML content
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find elements for posts, likes, comments, and saved
        #posts_element = soup.find("span", attrs={"class": "css-j2a19r-SpanText efbd9f0"})
        #posts = posts_element.text.strip() if posts_element else ""  # If there's no description, set it to blank
        likes = soup.find("span", attrs={"class": "xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk"}).text
        sharenlikes = soup.find("div", attrs={"class": "x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x1qjc9v5 xozqiw3 x1q0g3np xykv574 xbmpl8g x4cne27 xifccgj"}).text
        commentor_names = soup.find_all("span", attrs={"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u"})
        comments_texts = soup.find_all("div", attrs={"dir": "auto"})

        # Close the Chrome driver
        driver.quit()

        # Print the collected data
        print("The CSV file has been created")
        print("")

        with open("scrape_facebook.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Number of Likes", "Number of Comments and Shares", "Commentor Name", "Comment"])
            writer.writerow([likes+" Likes", sharenlikes])

            # Loop through all comments and write them to CSV
            for commentor_name, comment_text in zip(commentor_names, comments_texts):
                commentor_name_text = commentor_name.text.strip()
                comment_text_text = comment_text.text.strip()
                writer.writerow(["", "", commentor_name_text, comment_text_text])

        break

    else:
        print("Please wait until the page fully loads.")

