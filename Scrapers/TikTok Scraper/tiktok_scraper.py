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
        posts_element = soup.find("span", attrs={"class": "css-j2a19r-SpanText efbd9f0"})
        posts = posts_element.text.strip() if posts_element else ""  # If there's no description, set it to blank
        likes = soup.find("strong", attrs={"data-e2e": "like-count"}).text
        comments = soup.find("strong", attrs={"data-e2e": "comment-count"}).text
        saved = soup.find("strong", attrs={"data-e2e": "undefined-count"}).text
        share = soup.find("strong", attrs={"data-e2e": "share-count"}).text
        commentor_names = soup.find_all("span", attrs={"class": "css-1665s4c-SpanUserNameText e1g2efjf3"})
        comments_texts = soup.find_all("p", attrs={"class": "css-xm2h10-PCommentText e1g2efjf6"})

        # Close the Chrome driver
        driver.quit()

        # Print the collected data
        print("The CSV file has been created")
        print("")

        with open("scrape_tiktok.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Post Name", "Number of Likes", "Number of Comments", "Number of Saved", "Number of Shares", "Commentor Name", "Comment"])
            writer.writerow([posts, likes, comments, saved, share])

            # Loop through all comments and write them to CSV
            for commentor_name, comment_text in zip(commentor_names, comments_texts):
                commentor_name_text = commentor_name.text.strip()
                comment_text_text = comment_text.text.strip()
                writer.writerow(["", "", "", "", "", commentor_name_text, comment_text_text])

        break

    else:
        print("Please wait until the page fully loads.")

