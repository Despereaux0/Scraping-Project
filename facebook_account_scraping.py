from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

# Ask the user for the TikTok profile URL
facebook_url = input("Enter the Facebook profile URL: ")

# Ask the user for the number of posts to scrape
num_posts = int(input("Enter the number of posts to scrape: "))

# Initialize Chrome driver (you need to have chromedriver installed and in your PATH)
driver = webdriver.Chrome()

# Open the TikTok profile page
driver.get(facebook_url)

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
acc_name = soup.find("h1", attrs={"class": "html-h1 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1vvkbs x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz"}).text
acc_desc = soup.find("span", attrs={"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u"})
acc_stats = soup.find("span", attrs={"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa"}).text


# Write account information to the main CSV file
with open("scrape_facebook.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account Name", "Account Description", "Likes and Followers"])
    writer.writerow([acc_name, acc_desc, acc_stats])

# Find all the post elements
post_elements = driver.find_elements(By.CLASS_NAME, "x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lliihq x1pdlv7q")

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
    posts_element = soup.find("span", attrs={"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u"})
    posts = posts_element.text.strip() if posts_element else ""  # If there's no description, set it to blank
    likes = soup.find('span', attrs={'class': 'x1e558r4'}).text
    comments_shares = soup.find("span", attrs={"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa"}).text
    commentor_names = soup.find_all("span", attrs={"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u"})
    comments_texts = soup.find_all("a", attrs={"class": "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz xt0b8zv x1hl2dhg x1fey0fg"})

    # Write post-related information to the main CSV file in a new "sheet"
    with open("scrape_facebook.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([])  # Empty row to act as a separator between "sheets"
        writer.writerow(["Post Name", "Likes", "Comments and Shares", "Commentor", "Comment"])
        writer.writerow([posts, likes, comments_shared, "", ""])
        
        # Loop through all comments and write them to CSV
        for commentor_name, comment_text in zip(commentor_names, comments_texts):
            commentor_name_text = commentor_name.text.strip()
            comment_text_text = comment_text.text.strip()
            writer.writerow(["", "", "", commentor_name_text, comment_text_text])
            
    # Go back to the profile page to click on the next post
    driver.back()
    time.sleep(2)  # Wait for page to load fully

# Close the WebDriver
driver.quit()
print("Scraping Complete")

