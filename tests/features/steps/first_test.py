from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@given('website "{url}"')
def step(context, url):
    context.browser = webdriver.Firefox()
    context.browser.maximize_window()
    context.browser.get("http://localhost:8000/")


@then("push button with text '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'button'))
    )
    # try:
    #     context.browser.find_element_by_class_name('button').click()
    # except Exception as e:
    context.browser.find_element_by_class_name('button').click()



@then("login page '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    username = context.browser.find_element_by_name('username')
    username.clear()
    username.send_keys('john_user')
    password = context.browser.find_element_by_name('password')
    password.clear()
    password.send_keys('123456')
    enter = context.browser.find_element_by_name('enter')
    enter.click()
    assert context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text)


@then("page include '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    assert context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text)


@then("authentication '{name}'")
def step(context, name):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "%s")]' % name))
    )

    assert context.browser.find_element_by_xpath('//span[contains(text(), "%s")]' % name)


@then("go throught the links articles '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "%s")]' % text))
    )
    context.browser.find_element_by_xpath('//p[contains(text(), "%s")]' % text).click()


@then("check access to a edit article '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    assert context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text)


@then("do edit '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text).click()


@then("check edit '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    assert context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text)


@then("send edit '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    title = context.browser.find_element_by_name('title')
    title.clear()
    title.send_keys('REFACTOR OUR TITLE')
    text = context.browser.find_element_by_name('text')
    text.clear()
    text.send_keys('IT ATTRACTOR REFACTOR THE TEXT!!!')
    enter = context.browser.find_element_by_name('send_article')
    enter.click()


@then("delete article '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "%s")]' % text))
    )
    context.browser.find_element_by_xpath('//p[contains(text(), "%s")]' % text).click()


@then("do delete article '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text).click()


@then("do add article '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    try:
        context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text).click()
    except Exception as e:
        context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text).click()


@then("send add article '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    title = context.browser.find_element_by_name('title')
    title.clear()
    title.send_keys('NEW TITLE')
    text = context.browser.find_element_by_name('text')
    text.clear()
    text.send_keys('IT ATTRACTOR REFACTOR THE TEXT!!!\n IT ATTRACTOR REFACTOR THE TEXT!!!\n'
                   'IT ATTRACTOR REFACTOR THE TEXT!!!')
    enter = context.browser.find_element_by_name('add_article')
    enter.click()


@then("logout '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    try:
        context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text).click()
    except Exception as e:
        context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text).click()

#
# @then("again push button with text '{text}'")
# def step(context, text):
#     WebDriverWait(context.browser, 40).until(
#         EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "%s")]' % text))
#     )
#     context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text).click()
#

@then("wrong login '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    username = context.browser.find_element_by_name('username')
    username.clear()
    username.send_keys('john_user')
    password = context.browser.find_element_by_name('password')
    password.clear()
    password.send_keys('1234')
    enter = context.browser.find_element_by_name('enter')
    enter.click()
    assert context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text)


@then("assert error '{text}'")
def step(context, text):
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "%s")]' % text))
    )
    time.sleep(3)
    assert context.browser.find_element_by_xpath('//*[contains(text(), "%s")]' % text)
    context.browser.quit()


