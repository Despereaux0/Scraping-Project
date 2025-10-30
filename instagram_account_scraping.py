from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

# Ask the user for the TikTok profile URL
tiktok_url = input("Enter the TikTok profile URL: ")

# Ask the user for the number of posts to scrape
num_posts = int(input("Enter the number of posts to scrape: "))

# Initialize Chrome driver (you need to have chromedriver installed and in your PATH)
driver = webdriver.Chrome()

# Open the TikTok profile page
driver.get(tiktok_url)

while True:
    # Sleep until user enters 'Y'
    user_input = input("Enter 'Y' when the page has fully loaded (Solve the Captcha): ").strip().upper()
    if user_input == 'Y':
        break
    else:
        print("Please wait until the page fully loads.")

# Parse the HTML content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find elements for account information
acc_name = soup.find("h1", attrs={"data-e2e": "user-title"}).text
acc_desc = soup.find("h2", attrs={"data-e2e": "user-bio"}).text
acc_following = soup.find("strong", attrs={"data-e2e": "following-count"}).text
acc_followers = soup.find("strong", attrs={"data-e2e": "followers-count"}).text
acc_likes = soup.find("strong", attrs={"data-e2e": "likes-count"}).text

# Write account information to the main CSV file
with open("scrape_tiktok.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account Name", "Account Description", "Following", "Followers", "Likes"])
    writer.writerow([acc_name, acc_desc, acc_following, acc_followers, acc_likes])

# Find all the post elements
post_elements = driver.find_elements(By.CLASS_NAME, "css-1wrhn5c-AMetaCaptionLine")

# Limit the number of posts to scrape based on user input
num_posts = min(num_posts, len(post_elements))

for i in range(num_posts):
    post_element = post_elements[i]
    # Execute JavaScript to click on the post element
    driver.execute_script("arguments[0].click();", post_element)
    time.sleep(3)  # Wait for the post page to load
    
    # Parse the HTML content after clicking on the post
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find post-related information
    posts_element = soup.find("span", attrs={"class": "css-j2a19r-SpanText efbd9f0"})
    posts = posts_element.text.strip() if posts_element else ""  # If there's no description, set it to blank
    likes = soup.find('strong', attrs={'data-e2e': 'browse-like-count'}).text
    comments = soup.find("strong", attrs={"data-e2e": "browse-comment-count"}).text
    saved = soup.find("strong", attrs={"data-e2e": "undefined-count"}).text
    commentor_names = soup.find_all("span", attrs={"data-e2e": "comment-username-1"})
    comments_texts = soup.find_all("p", attrs={"data-e2e": "comment-level-1"})

    # Write post-related information to the main CSV file in a new "sheet"
    with open("scrape_tiktok.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([])  # Empty row to act as a separator between "sheets"
        writer.writerow(["Post Name", "Likes", "Comments", "Saved", "Commentor", "Comment"])
        writer.writerow([posts, likes, comments, saved, "", ""])
        
        # Loop through all comments and write them to CSV
        for commentor_name, comment_text in zip(commentor_names, comments_texts):
            commentor_name_text = commentor_name.text.strip()
            comment_text_text = comment_text.text.strip()
            writer.writerow(["", "", "", "", commentor_name_text, comment_text_text])
            
    # Go back to the profile page to click on the next post
    driver.back()
    time.sleep(2)  # Wait for page to load fully

# Close the WebDriver
driver.quit()
print("Scraping Complete")

