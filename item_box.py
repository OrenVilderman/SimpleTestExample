from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

class ItemBox:
    def __init__(self, name):
        self.name = name
        self.price = 0.0
        self.description = ''

        chrome_driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

        chrome_driver.get('https://www.saucedemo.com/inventory.html')
        chrome_driver.maximize_window()

        sk_element = chrome_driver.find_element_by_class_name("login_password").text
        start = sk_element.find('\n') + 1
        sk = sk_element[start:]

        user_element = chrome_driver.find_element_by_class_name("login_credentials").text
        start = user_element.find('\n') + 1
        end = user_element.find('\n',start+1)
        user = user_element[start:end]

        chrome_driver.find_element_by_id("user-name").send_keys(user)
        chrome_driver.find_element_by_id("password").send_keys(sk)
        chrome_driver.find_element_by_id("login-button").click()

        item_element_arr = chrome_driver.find_elements_by_xpath("//*[@class='inventory_list']/div[@class='inventory_item']")

        items = {}
        for item in item_element_arr:
            item_str = item.text
            end = item_str.find('\n')
            name = item_str[:end]

            if(self.name == name):
                item_str = item.text
                start = item_str.find('$') + 1
                end = item_str.find('\n', start + 1)
                price = item_str[start:end]
                self.price = float(price)

                item_str = item.text
                start = item_str.find('\n') + 1
                end = item_str.find('$') - 1
                self.description = item_str[start:end]

                break

        #Sleep here since without it, the test might be to fast to see and this is only a demo of a test
        sleep(2)
        chrome_driver.close()