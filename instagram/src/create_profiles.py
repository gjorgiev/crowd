import sys
sys.path.append('.')
from common.tools.utils import setup_chrome_mobile
from common.tools.utils import save_line_to_file
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import string
from names import get_full_name
import os
import pickle

class Button:

    def __init__(self, driver):
        self.driver = driver

    def goto_instagram(self):
        # navigate to instagram.com
        self.driver.get('http://www.instagram.com')
        print('Go to instagram')

    def __click_button(self, xpath):
        try:
            button = self.driver.find_element_by_xpath(xpath)
            actions = ActionChains(driver)
            actions.pause(random.randint(1,3))
            actions.move_to_element(button)
            actions.pause(random.randint(1,3))
            actions.click(button)
            actions.perform()
            print(xpath + ' button clicked!')
        except NoSuchElementException as ex:
            print(ex + "\nClass: " + self.__class__.__name__ + "\n Function: " + __name__)

    def click_signup(self):
        self.__click_button("//button[text()='Sign up with email or phone number']")

    def click_email(self):
        self.__click_button("//span[text()='Email']")
    
    def click_skip(self):
        self.__click_button("//button[text()='Skip']")
    
    def click_next(self):
        self.__click_button("//button[text()='Next']")

class Input:

    def __init__(self, driver):
        self.driver = driver
        
    def __enter_data(self, name, data):
        try:
            input = self.driver.find_element_by_name(name)
            actions = ActionChains(driver)
            actions.pause(random.randint(1,3))
            actions.move_to_element(input)
            print("Entering data:" + data + " in input field: " + name)
            for item in data:
                actions.send_keys_to_element(input, item)
                actions.pause(random.randint(1,3))
            actions.perform()
            print("\nEntered Data: " + data + "\nInput name: " + name)
        except NoSuchElementException as ex:
            print(ex + "\nClass: " + self.__class__.__name__ + "\n Function: " + __name__)

    def enter_email(self, email):
        self.__enter_data("email", email)
    
    def enter_fullname(self, fullname):
        self.__enter_data("fullName", fullname)

    def enter_password(self, password):
        self.__enter_data("password", password)

class RandomGenerator:

    def __init__(self):
        super().__init__()
        
    def generate_random_password(self, size=10):
        password = ''.join(random.choice(string.ascii_lowercase+string.digits+'@$#') for i in range(size))
        print ("Generated password: " + password)
        return password

    def generate_random_email(self, size=9, operator="@hotmail.com"):
        email = ''.join(random.choice(string.ascii_lowercase+string.digits+'_.') for i in range(size)) + operator
        print ("Generated email: " + email)
        return email

class Profile:

    def __init__(self, driver):
        self.cookies_path = "instagram\\data\\cookies"
        self.accounts_path = "instagram\\data\\accounts.txt"
        self.rnd_gen = RandomGenerator()
        self.button = Button(driver)
        self.input = Input(driver)
        self.email = self.rnd_gen.generate_random_email()
        self.password = self.rnd_gen.generate_random_password()
        self.fullname = get_full_name()

    def __save_cookies(self):
        cookies_filepath = self.cookies_path + "\\" + self.email + '.pkl'
        pickle.dump(driver.get_cookies(), open(cookies_filepath,"wb"))
        print("Cookies for email: " + self.email + " have been saved to " + cookies_filepath)

    def __save_to_file(self):
        save_line_to_file(self.accounts_path, self.email + ',' + self.password + ',' + self.fullname)

    def __save_profile(self):
        self.__save_cookies()
        self.__save_to_file()
    
    def __navigate(self):
        self.button.goto_instagram()
        self.button.click_signup()
        self.button.click_email()
        self.input.enter_email(self.email)
        self.button.click_next()
        self.input.enter_fullname(self.fullname)
        self.input.enter_password(self.password)
        self.button.click_next()
        self.button.click_next()
        self.button.click_skip()

    def create(self):
        self.__navigate()
        self.__save_profile()

driver = setup_chrome_mobile()
profile = Profile(driver)
profile.create()