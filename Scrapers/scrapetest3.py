from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

# Initialize Chrome driver (you need to have chromedriver installed and in your PATH)
driver = webdriver.Chrome()

# Open the TikTok profile page
driver.get("https://www.tiktok.com/@acsonmalaysia")

# Sleep for a few seconds to ensure that the page loads completely
time.sleep(20)

# Parse the HTML content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find views and followers
accname = soup.find("h1", attrs={"data-e2e": "user-title"})
following = soup.find("strong", attrs={"data-e2e": "following-count"})
followers = soup.find("strong", attrs={"data-e2e": "followers-count"})
likes = soup.find("strong", attrs={"data-e2e": "likes-count"})

posts = soup.find_all("span", attrs={"class": "css-j2a19r-SpanText efbd9f0"})
views = soup.find_all("strong", attrs={"data-e2e": "video-views"})

# Close the Chrome driver
driver.quit()

# Check if posts list is not empty
if posts:
    # Use find_all instead of find
    print("Account Name:", accname.text.strip())
    print("Following:", following.text.strip())
    print("Followers:", followers.text.strip())
    print("Likes:", likes.text.strip())

    # Open CSV file for writing
    with open("scrape_tiktok.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account Name", "Following", "Followers", "Likes"])
        writer.writerow([accname.text.strip(), following.text.strip(), followers.text.strip(), likes.text.strip()])
        writer.writerow([])  # Empty row for spacing
        writer.writerow(["Post", "Views"])
        
        # Loop through all video views and print them
        for post, view in zip(posts, views):
            post_text = post.text.strip()
            view_text = view.text.strip()
            if post_text:  # Check if post text is not empty
                print("Post:", post_text)
                print("Views:", view_text)
                writer.writerow([post_text, view_text])

    print("CSV file 'tiktok_data.csv' has been created.")
else:
    print("No posts found.")
