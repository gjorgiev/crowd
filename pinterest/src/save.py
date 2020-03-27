import sys
sys.path.append('.')
from common.tools.utils import setup_chrome_mobile_cookie
from common.tools.utils import save_line_to_file
from common.tools.utils import read_file_as_array
from common.tools.utils import read_first_line
from common.tools.utils import remove_text_from_file
from common.tools.utils import remove_first_line
from common.tools.utils import read_random_line
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
import string
import os
import pickle
from multiprocessing import Pool
from multiprocessing import Queue
from multiprocessing import Process
from multiprocessing import Lock

class Button:
    
    def __init__(self, driver):
        self.driver = driver

    def __click_button(self, xpath):
        try:
            button = self.driver.find_element_by_xpath(xpath)
            actions = ActionChains(self.driver)
            actions.move_to_element(button)
            actions.click(button)
            actions.perform()
            print('click: ' + xpath)
            return True
        except NoSuchElementException as ex:
            print(ex)
            return False

    def click_react(self):
        self.__click_button("//div[@class='Jea X6t zI7 iyn Hsu']")

    def click_emoji(self):
        emojies = self.driver.find_elements_by_xpath("//div[@class='Jea Z2K zI7 iyn Hsu']")
        size = len(emojies)
        print("emojies size is " + str(size))
        if size > 0:
            idx = random.randint(0, size-2)
            print("idx = " + str(idx))
            emoji = emojies[idx]
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(emoji)
                actions.move_to_element(emoji)
                actions.click(emoji)
                actions.click(emoji)
                actions.click(emoji)
                actions.perform()
            except NoSuchElementException as ex:
                print(ex)

    def click_save(self):
        return self.__click_button("//span[@title='Save']")

    def click_continue(self):
        self.__click_button("//div[@data-test-id='appUpsell-continue']")

    def click_createboard(self):
        self.__click_button("//div[text()='Create board']")

    def click_create(self):
        self.__click_button("//div[text()='Create']")
        sleep(3)

class Input:

    def __init__(self, driver):
        self.driver = driver

    def __enter_data(self, id, data):
        try:
            input = self.driver.find_element_by_id(id)
            actions = ActionChains(self.driver)
            actions.move_to_element(input)
            actions.send_keys_to_element(input, data)
            actions.perform()
            print("\ndata:" + data + "\nfield: " + id)
        except NoSuchElementException as ex:
            print(ex)
    
    def enter_boardname(self, board_name):
        self.__enter_data("boardNameInput", board_name)

# read the pin file # input("Enter Pin: ")
pin = read_first_line("pinterest\\data\\pin.txt")
print(pin)
# define path for saved pins
saved_path = "pinterest\\data\\saved\\"
# set pin file name
pin_filename = ''.join(filter(str.isdigit, pin)) + '.txt'
# saved pins
saved = read_file_as_array(saved_path + pin_filename)

# save profile in folder \saved 
def save_as_pinned(cookie):
    lock = Lock()
    lock.acquire()
    save_line_to_file(saved_path + pin_filename, cookie + '\n')
    lock.release()

def has_repinned(name):
    try:
        with open(os.path.join(saved_path, pin_filename), 'r') as pin_file:
            for pin in pin_file:
                if name in pin:
                    return True
    except FileNotFoundError:
        pass
    return False

# define boards path
boards_path = "pinterest\\data\\boards.txt"
# lock to use for reading and saving files 

def choose_board_name():
    lock = Lock()
    lock.acquire()
    board = read_first_line(boards_path)
    remove_first_line(boards_path)
    lock.release()
    return board

cookies_path = "pinterest\\cookies"
cookies = os.listdir(cookies_path)

def do_save_action(driver, cookie):
    driver.get(pin)
    button = Button(driver)
    if not button.click_save():
        #os.remove(cookies_path + "\\" + cookie)
        driver.close()
        driver.quit()
        return
    sleep(1)
    button.click_continue()
    button.click_createboard()
    _input = Input(driver)
    board = choose_board_name()
    _input.enter_boardname(board)
    button.click_create()
    save_as_pinned(cookie)
    sleep(1)
    button.click_react()
    sleep(3)
    button.click_emoji()
    sleep(1)
    watch = random.randint(300, 500)
    print("watch time: " + str(watch))
    sleep(watch)
    driver.close()
    driver.quit()

def has_connection(driver):
    try:
        driver.find_element_by_xpath('//span[@jsselect="heading" and @jsvalues=".innerHTML:msg"]')
        return False
    except: return True

def run(cookie):
    # check if already has been saved the pin
    if not has_repinned(cookie):
        print(cookie)
        driver = setup_chrome_mobile_cookie(cookies_path, cookie)
        if has_connection(driver):
            do_save_action(driver, cookie)
        else:
            driver.close()
            driver.quit()

def run_pool(processes = 5):
    with Pool(processes=processes) as pool:
        pool.map(run, cookies)
        pool.close()
        pool.join()

if __name__ == '__main__':
    run_pool()
