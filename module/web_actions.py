#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class WebAction:
    def __init__(self, driver):
        self.webdriver = driver
        self.element_wait_time = 30
        self.webdriver_wait = WebDriverWait(self.webdriver, self.element_wait_time)
        self.temp_save = {}

    @classmethod
    def sleep(cls, wait_time):
        time.sleep(wait_time)

    def url(self, url):
        self.webdriver.get(url)

    def wait_element(self, func):
        try:
            return self.webdriver_wait.until(lambda x: func)
        except Exception as e:
            print(e)
            with allure.step('未发现元素截图'):
                allure.attach(self.webdriver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
            return False

    def assert_result(self, result, step_message):
        if result is False:
            with allure.step(step_message):
                allure.attach(self.webdriver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)

    def find_element(self, value):
        return self.wait_element(self.webdriver.find_element_by_xpath(value))

    def get_element_attribute(self, value, attribute):
        element = self.find_element(value)
        return element.get_attribute(attribute)

    def click_element(self, value):
        element = self.find_element(value)
        self.find_element(value).click()
        return element

    def send_element(self, value, message):
        element = self.find_element(value)
        self.find_element(value).send_keys(message)
        return element

    def clear_element(self, value):
        element = self.find_element(value)
        element.clear()
        return element

    def click_accept_alert(self, value):
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: ec.alert_is_present())
        alert.accept()

    def click_cancel_alert(self, value):
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: ec.alert_is_present())
        alert.dissmiss()

    def click_send_keys_accept_alert(self, value, message):
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: ec.alert_is_present())
        alert.sendKeys(message)
        alert.accept()

    def click_send_keys_cancel_alert(self, value, message):
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: ec.alert_is_present())
        alert.sendKeys(message)
        alert.dissmiss()

    def switch_iframe(self, value):
        iframe = self.find_element(value)
        self.webdriver.switch_to.frame(iframe)

    def switch_default_iframe(self):
        self.webdriver.switch_to.default_content()

    def switch_default_page(self):
        handles = self.webdriver.window_handles
        self.webdriver.switch_to_window(handles[0])

    def switch_new_page(self):
        handles = self.webdriver.window_handles
        self.webdriver.switch_to_window(handles[1])
