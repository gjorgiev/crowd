import pickle
from selenium import webdriver
import time
import random
import sys
sys.path.append('.')
import utils
import os
from selenium.common.exceptions import NoSuchElementException

cookies = "instagram\\data\\cookies"
accounts = open("instagram\\data\\accounts.txt","r")
files = os.listdir(cookies)
random_sleep = random.randrange(1,3)

for account in accounts:
    line = account.split(',')
    email_value = line[0]
    password_value = line[1]
    if len(email_value) > 1:
        file_path = os.path.join(cookies, email_value)
        file_path += '.pkl'
        
        if email_value + '.pkl' in files:
            print(file_path + ' already exists')
            continue

        print('Working on ' + email_value + ' to save in ' + file_path)
        
        driver = utils.setup_chrome_mobile()
        driver.get("http://www.instagram.com")

        try:
            time.sleep(random_sleep)
            driver.find_element_by_xpath("//button[@type='button']").click()
            time.sleep(random_sleep)
            driver.find_element_by_name("username").send_keys(email_value)
            time.sleep(random_sleep)
            driver.find_element_by_name("password").send_keys(password_value)
            time.sleep(random_sleep)
            driver.find_element_by_xpath("//button[@type ='submit']").click()
            time.sleep(random_sleep)
            pickle.dump(driver.get_cookies(), open(file_path,"wb"))
        except NoSuchElementException as ex:
            print(ex)
        driver.close()

accounts.close()