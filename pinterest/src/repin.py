import sys
sys.path.append('.')
import os
import time
from common.tools.utils import setup_chrome
import random
import pickle
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from common.tools.utils import cookie_driver
from common.tools.utils import save_line_to_file

def read_board_names():
    boards_file = open(os.path.join('boards', 'boards.txt'), 'r')
    board_names = []
    for board_name in boards_file:
        board_names.append(board_name)
    boards_file.close()
    return board_names

def read_repin_links():
    to_repin_files = open(os.path.join('repins', 'repins.txt'), 'r')
    to_repin_links = []
    for to_repin_link in to_repin_files:
        to_repin_links.append(to_repin_link)
    to_repin_files.close()
    return to_repin_links

def has_repinned(name, repin_filename):
    try:
        with open(os.path.join('repins', repin_filename), 'r') as repin_file:
            for repin in repin_file:
                if name in repin:
                    return True
    except FileNotFoundError:
        pass
    return False

def is_board_created(name):
    try:
        with open(os.path.join('boards', 'created.txt'), 'r') as created_file:
            for created in created_file:
                if name in created:
                    print("board name: " + name + " has already been created. ")
                    return True
    except FileNotFoundError:
        pass
    return False

def click_save_button(driver):
    # click save button or cicle around it for first timers
    try:
        print('Saving pin: ' + pin + ' to user: ' + name)
        driver.find_element_by_xpath("//div[@data-test-id='SaveButton']").click()
        print('Saved!')
        return True
    except NoSuchElementException as exception:
        print(exception)
        try:
            driver.find_element_by_xpath("//button[@data-test-id='PinBetterSaveButton']").click()
            print('Saved!')
            return True
        except NoSuchElementException as ex:
            print(ex)
        except ElementClickInterceptedException as ex:
            print(ex)
    except ElementClickInterceptedException as exception:
        print(exception)
        try:
            driver.find_element_by_xpath("//div[@class='DgX Hsu']").click()
            print('Saved!')
            return True
        except NoSuchElementException as exception:
            print(exception)
        except ElementClickInterceptedException as exception:
            print(exception)
    return False

def choose_board(driver):
    # choose new board for the pin
    try:
        li = driver.find_elements_by_tag_name('li')
        if len(li) > 0:
            li[random.randrange(0, len(li))].click()
            driver.find_element_by_xpath("//button[@type='submit']").click()
    except NoSuchElementException as ex:
        print(ex)
    except ElementClickInterceptedException as ex:
        print(ex)

def create_board(driver):
    board_names = read_board_names()
    for board_name in board_names:
        if not is_board_created(board_name):
            try:
                print ("Saving in board: " + board_name)
                # click on drop down list
                try:
                    driver.find_element_by_xpath("//button[@data-test-id='PinBetterSaveDropdown']").click()
                    # click on create board
                    driver.find_element_by_xpath("//div[@data-test-id='create-board']").click()
                except NoSuchElementException as ex:
                    button = driver.find_element_by_xpath("//div[@data-test-id='SaveButton']")
                    actions = ActionChains(driver)
                    actions.move_to_element(button)
                    actions.click(button)
                    actions.perform()
                    # click on create board
                    try:
                        driver.find_element_by_xpath("//div[@data-test-id='createBoardButton']").click()
                    except NoSuchElementException as ex:
                        print(ex)
                    else:
                        try:
                            driver.find_element_by_xpath("//button[@type='submit']").click()
                        except NoSuchElementException as ex:
                            driver.find_element_by_xpath("//button[@type='button']").click()
                            print(ex)
                            time.sleep(4)
                # write board name
                driver.find_element_by_id("boardEditName").send_keys(board_name)
                # click submit
                try:
                    driver.find_element_by_xpath("//button[@type='submit']").click()
                except NoSuchElementException as ex:
                    driver.find_element_by_xpath("//button[@type='button']").click()
                    print(ex)
                time.sleep(4)
            except NoSuchElementException as ex:
                print(ex)
            except ElementClickInterceptedException as ex:
                print(ex)
            except StaleElementReferenceException as ex:
                print(ex)
            except WebDriverException as ex:
                print(ex)
            return board_name


def save_pin(name, pin):
    # redirect to pin
    driver = cookie_driver(name)
    driver.get(pin)
    driver.execute_script
    print ("Saving pin: " + pin + " to " + name)
    board_name = create_board(driver)
    save_line_to_file(os.path.join('boards', 'created.txt'), board_name)
    #click_save_button(driver)
    #choose_board(driver)
    driver.close()

to_repin_links = read_repin_links()

for pin in to_repin_links:
    files = os.listdir('cookies')

    for name in files:
        # check if pin is already repinned from the user
        repin_filename = ''.join(filter(str.isdigit, pin)) + '.txt'
        if has_repinned(name, repin_filename):
            continue
        save_pin(name, pin)
        save_line_to_file(os.path.join('repins', repin_filename), name + '\n')
        