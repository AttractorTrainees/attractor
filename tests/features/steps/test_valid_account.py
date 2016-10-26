# from behave import *
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
#
#
# @given('website "{url}"')
# def step(context, url):
# #Измените строку, для выполнения теста в другом браузере
#     context.browser = webdriver.Firefox()
#     context.browser.maximize_window()
#     context.browser.get("http://localhost:8000/")
#
#
#
# @then('I will see the account details')
# def step_impl(context):
#     elements = find_elements(context.browser, id='no-account')
#     eq_(elements, [], 'account not found')
#     h = get_element(context.browser, id='account-head')
#     ok_(h.text.startswith("Account 61415551234"),
#         'Heading %r has wrong text' % h.text)
