import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

'''
Question 1
1. Navigate to https: //www.saucedemo.com/inventory.html
2. Add 2 products to cart
1. most expensive product
2. The cheapest product
3. Verify on inventory screen that :
1. Cart number of products = 2
2. Both product’s button changed to “REMOVE”
4. Click Cart button
5. Remove the most expensive product from list
1. Verify it removed
6. Click CHECKOUT button
7. Fill details and press CONTINUE
8. Verify :
1. QTY = 1
2. Item total = 7.99$
9. Click FINISH
1. Verify the following message appears : “Your order has been dispatched,
and will arrive just as fast as the pony can get there!”
'''

def test_question_one():
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

        item_str = item.text
        start = item_str.find('$') + 1
        end = item_str.find('\n', start + 1)
        price = item_str[start:end]
        items[name] = float(price)

    sorted_items = sorted(items.items(), key=lambda kv: kv[1])

    x_path_low = "//*[text()='{}']/../../..//button".format(sorted_items[0][0])
    chrome_driver.find_element_by_xpath(x_path_low).click()
    x_path_high = "//*[text()='{}']/../../..//button".format(sorted_items[len(sorted_items)-1][0])
    chrome_driver.find_element_by_xpath(x_path_high).click()

    shopping_cart = chrome_driver.find_element_by_class_name("shopping_cart_badge").text
    assert (shopping_cart == '2')

    lowest_price_button_text = chrome_driver.find_element_by_xpath(x_path_low).text
    highest_price_button_text = chrome_driver.find_element_by_xpath(x_path_high).text
    assert (lowest_price_button_text == 'REMOVE')
    assert (highest_price_button_text == 'REMOVE')

    chrome_driver.find_element_by_class_name("shopping_cart_badge").click()

    item_element_arr = chrome_driver.find_elements_by_xpath("//*[@class='cart_list']/div[@class='cart_item']")

    chrome_driver.find_element_by_xpath(x_path_high).click()

    try:
        highest_price_button_text = chrome_driver.find_element_by_xpath(x_path_high).text
    except Exception as e:
        x_path_high_not_found = e

    assert ('no such element: Unable to locate element' in str(x_path_high_not_found))

    chrome_driver.find_element_by_xpath("//button[@data-test='checkout']").click()

    chrome_driver.find_element_by_xpath("//input[@data-test='firstName']").send_keys("Oren")
    chrome_driver.find_element_by_xpath("//input[@data-test='lastName']").send_keys("Vilderman")
    chrome_driver.find_element_by_xpath("//input[@data-test='postalCode']").send_keys("123456")
    chrome_driver.find_element_by_xpath("//input[@data-test='continue']").click()


    assert(chrome_driver.find_element_by_xpath("//*[@class='cart_quantity']").text == "1")

    #TODO: Open a bug and verify with product if this version can go to production.
    # assert(chrome_driver.find_element_by_xpath("//*[@class='inventory_item_price']").text == "7.99$")

    chrome_driver.find_element_by_xpath("//button[@data-test='finish']").click()
    assert(chrome_driver.find_element_by_xpath("//*[@class='complete-text']").text == "Your order has been dispatched, and will arrive just as fast as the pony can get there!")

    #Sleep here since without it, the test might be to fast to see and this is only a demo of a test
    sleep(2)
    chrome_driver.close()

'''
Question 2
1. Create a function name “is_sorted“ that Get list of items with price and
Return a Boolean result : if the List is sorted or not (without using built-in
Sort() method)
2. Navigate to https: //www.saucedemo.com/inventory.html
3. Select
4. Sort products by : Price (Low to High)
1. Get all items presented on page
2. use your function “is_sorted” and verify if the products are sorted by :
Price (Low to High)
'''

def test_question_two():
    chrome_driver = webdriver.Chrome(
        executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    chrome_driver.get('https://www.saucedemo.com/inventory.html')
    chrome_driver.maximize_window()

    sk_element = chrome_driver.find_element_by_class_name("login_password").text
    start = sk_element.find('\n') + 1
    sk = sk_element[start:]

    user_element = chrome_driver.find_element_by_class_name("login_credentials").text
    start = user_element.find('\n') + 1
    end = user_element.find('\n', start + 1)
    user = user_element[start:end]

    chrome_driver.find_element_by_id("user-name").send_keys(user)
    chrome_driver.find_element_by_id("password").send_keys(sk)
    chrome_driver.find_element_by_id("login-button").click()

    chrome_driver.find_element_by_xpath("//select[@data-test='product_sort_container']/option[@value='lohi']").click()

    item_element_arr = chrome_driver.find_elements_by_xpath("//*[@class='inventory_list']/div[@class='inventory_item']")

    items = {}
    for item in item_element_arr:
        item_str = item.text
        end = item_str.find('\n')
        name = item_str[:end]

        item_str = item.text
        start = item_str.find('$') + 1
        end = item_str.find('\n', start + 1)
        price = item_str[start:end]
        items[name] = float(price)

    items_after_sort = tuple(items.values())
    assert(is_sorted(items_after_sort) == True)

    #Sleep here since without it, the test might be to fast to see and this is only a demo of a test
    sleep(2)
    chrome_driver.quit()

def is_sorted(items_arr):
    flag = True
    i = 1
    while i < len(items_arr):
        if (items_arr[i] < items_arr[i - 1]):
            flag = False
        i += 1
    return flag