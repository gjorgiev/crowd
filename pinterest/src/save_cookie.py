import pickle
from selenium import webdriver
import time
import random
from tools.utils import setup_chrome
import os
from selenium.common.exceptions import NoSuchElementException

path = "cookies"
accounts = open("pinterestaccs.txt","r")
files = os.listdir(path)

for account in accounts:
    email_value = account.split(',')[0]
    if len(email_value) > 1:
        file_path = os.path.join(path, email_value)
        file_path += '.pkl'
        
        if email_value + '.pkl' in files:
            print(file_path + ' already exists')
            continue

        print('Working on ' + email_value + ' to save in ' + file_path)
        
        driver = setup_chrome()
        driver.get("http://www.pinterest.com")

        try:
            driver.find_element_by_xpath("//div[text()='Log in']").click()
            time.sleep(2)
            driver.find_element_by_id("email").send_keys(email_value)
            driver.find_element_by_id("password").send_keys("password1234")
            time.sleep(2)
            driver.find_element_by_xpath("//button[@type ='submit']").click()
            time.sleep(5)
            pickle.dump(driver.get_cookies(), open(file_path,"wb"))
        except NoSuchElementException:
            pass
        driver.close()

accounts.close()