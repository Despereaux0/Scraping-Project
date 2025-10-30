from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException


user_search_2 = input("Enter the Google Sheet for the data:")


driver = webdriver.Chrome()
driver.get(user_search_2)

user_input = input("Enter 'Y' or 'y' once the page has loaded : ")
if user_input.lower() == 'y':

    
    plus_button = driver.find_element(By.XPATH, "//div[text()='docs-material goog-inline-block docs-sheet-button-inner-box']")


else:
    print("Please wait for the page to load")
