import pickle
import selenium.webdriver
import random
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from utils import save_line_to_file
from utils import remove_text_from_file
from utils import remove_newline
import os
from utils import setup_chrome

# BASE PATH CONSTANTS
PINTEREST_URL = "https://pinterest.com/pin/create/button/"
COOKIES_PATH = 'cookies'
PINS_PATH = 'pins'
IMAGES_PATH = 'images'
TMP_FOLDER_NAME = 'tmp'
LOCK_FILE_NAME = 'lock.txt'
LOCK_FILE_PATH = os.path.join(TMP_FOLDER_NAME, LOCK_FILE_NAME)
POSTS_PATH = os.path.join('posts', 'posts.txt')

files = os.listdir(COOKIES_PATH)
pins_files = os.listdir(PINS_PATH)

def random_post_and_board():
    # read the posts.txt file 
    posts_file = open(POSTS_PATH)
    # create empty list for the posts
    posts_list = []
    # append all lines from textfile to list
    for post in posts_file:
        posts_list.append(post)
    # close the file
    posts_file.close()
    # use random function to choose number from 0 to size of list
    index = random.randrange(0, len(posts_list))
    # return the splitted text
    return posts_list[index].split(',')[0], remove_newline(posts_list[index].split(',')[1])

def random_image(post_url):
    # read file with image links
    images = open(os.path.join(IMAGES_PATH, post_url.replace('https://bamboa.co/product/','') + '.txt'), 'r')
    # init empty images list
    images_list = []
    # append all lines to images list
    for image in images:
        images_list.append(image)
    # close image file
    images.close()
    return images_list[random.randrange(0, len(images_list))]


def locked(name):
    with open(LOCK_FILE_PATH, 'r') as lock:
        for line in lock:
            if name in line:
                return True
        return False

def lock(name):
    save_line_to_file(LOCK_FILE_PATH, name)

def unlock(name):
    remove_text_from_file(name, LOCK_FILE_PATH)

def cookie_driver(name):
    driver = setup_chrome()
    driver.get("http://www.google.com")
    time.sleep(random.randrange(1, 3))
    # load cookies for account
    cookies = pickle.load(open(os.path.join(COOKIES_PATH, name), "rb"))
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)
    return driver

for name in files:
    post_url, board_name = random_post_and_board()
    exist = False
    email_txt = name.replace('.pkl','.txt')
    pin_file = os.path.join(PINS_PATH, email_txt)
    # make sure that post_url is not published before
    if email_txt in pins_files:
        open_file = open(pin_file, 'r')
        for line in open_file:
            if post_url in line:
                exist = True
                break
        open_file.close()
        if exist:
            print(post_url + " already exist for user: " + name)
            continue
    
    if locked(name):
        print(name + " is locked")
        continue
    else:
        print("Execution information:")
        print(name)
        # lock current account
        lock(name)
        driver = cookie_driver(name)
        # open page for creating pin from website
        pin_url = PINTEREST_URL + '?url=' + post_url + '/&media=' + random_image(post_url)
        driver.get(pin_url)
        time.sleep(5)
        # check if board already exists
        list_boards = driver.find_elements_by_xpath("//div[@data-test-id='board-selection']/div/div/div[2]/div[1]")
        for board in list_boards:
            try:
                if board.text == board_name:
                    time.sleep(1)
                    board.click()
                    print(post_url + " added to board: " + board.text)
                    time.sleep(5)
            except StaleElementReferenceException:
                pass

        # click on create board if it exists and create new board
        # otherwise do nothing
        try:
            driver.find_element_by_xpath("//div[@data-test-id='createBoardButton']").click()
            time.sleep(2)
            driver.find_element_by_id("boardEditName").send_keys(board_name)
            time.sleep(2)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            print("Created new board and added pin")
            print("Board name: " + board_name)
            print("Post url: " + post_url)
            time.sleep(3)
            save_line_to_file(pin_file, pin_url)
        except (TimeoutException, NoSuchElementException):
            pass

        # see the created post
        try:
            seeitnow = driver.find_element_by_xpath("//div[text() = 'See it now']")
            seeitnow.click()
            time.sleep(2)
            save_line_to_file(pin_file, pin_url)
        except:
            pass

        time.sleep(5)
        unlock(name)
        driver.close()
