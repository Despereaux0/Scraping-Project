from bs4 import BeautifulSoup
import requests
import csv

page_to_scrape = requests.get("https://www.facebook.com/AcsonMalaysia")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
post = soup.findAll("div", attrs={"dir":"auto"})
likes = soup.findAll("span", attrs={"class":"x1e558r4"})
comments= soup.findAll("small", attrs={"class":"author"})
shares = soup.findAll("small", attrs={"class":"author"})


file = open("scraped_quotes.csv", "w")
writer = csv.writer(file)

writer.writerow(["Quotes", "Authors"])

for quote, author in zip(quotes, authors):
    #print(f"{quote.text} - {author.text}")
    #writer.writerow([quote.text, author.text])

file.close()

print(likes)
print(post)
