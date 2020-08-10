#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import allure
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# 方法用来做判断
from selenium.webdriver.support import expected_conditions as EC
from module.extend import Extend

PATH = os.path.dirname(os.path.abspath(__file__))
PIC_PATH = os.path.abspath(PATH + "/../pic")


class WebAction:
    def __init__(self, driver):
        self.webdriver = driver
        self.element_wait_time = 5
        self.webdriver_wait = WebDriverWait(self.webdriver, timeout=self.element_wait_time)
        self.temp_save = {}
        self.extend = Extend(self.webdriver)

    @classmethod
    def sleep(cls, wait_time):
        time.sleep(wait_time)

    def url(self, url):
        self.webdriver.get(url)

    def wait_element(self, value):
        try:
            return self.webdriver_wait.until(EC.presence_of_element_located((By.XPATH, value)))
        except Exception as e:
            with allure.step('未发现元素截图'):
                allure.attach(self.webdriver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
            assert False, "Not Found The Element " + value

    def assert_result(self, result, step_message):
        if result is False:
            with allure.step(step_message):
                allure.attach(self.webdriver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)

    def find_element(self, value):
        return self.wait_element(value)

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
        alert = self.webdriver_wait.until(lambda x: EC.alert_is_present())
        alert.accept()

    def click_cancel_alert(self, value):
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: EC.alert_is_present())
        alert.dissmiss()

    def click_send_keys_accept_alert(self, value, message):
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: EC.alert_is_present())
        alert.sendKeys(message)
        alert.accept()

    def click_send_keys_cancel_alert(self, value, message):
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: EC.alert_is_present())
        alert.sendKeys(message)
        alert.dissmiss()

    def switch_iframe(self, value):
        try:
            self.webdriver_wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, value)))
        except Exception as e:
            with allure.step('未发现元素截图'):
                allure.attach(self.webdriver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
            assert False, "Not Found The iframe " + value

    def switch_default_iframe(self):
        self.webdriver.switch_to.default_content()

    def switch_default_page(self):
        handles = self.webdriver.window_handles
        self.webdriver.switch_to_window(handles[0])

    def switch_new_page(self):
        handles = self.webdriver.window_handles
        self.webdriver.switch_to_window(handles[1])

    def print_title(self):
        title = self.webdriver.title
        print("Title is ", title)
        return title

    def assert_title(self, title):
        now_title = self.webdriver.title
        if now_title != title:
            msg = "当前页面title不为：" + title
            self.assert_result(False, msg)
            assert False

    def click_element_change(self, value):
        element = self.find_element(value)
        # 截图
        self.extend.get_screen_shot_by_element(element)
        # 修改截图位置
        pic_path = self.extend.write_to_file(PIC_PATH, value)
        # 点击
        element.click()
        # 新截图
        self.extend.get_screen_shot_by_element(element)
        same_result = self.extend.same_as(self.extend.load_image(pic_path))
        if same_result:
            msg = "元素" + value + "点击后没有变化"
            self.assert_result(False, msg)

    def save_attribute(self, key, value, attribute):
        attribute_value = self.get_element_attribute(value, attribute)
        if self.temp_save:
            self.temp_save[key] = attribute_value
        else:
            self.temp_save = {key: attribute_value}

    def check_attribute_change(self, key, value, attribute):
        attribute_value = self.get_element_attribute(value, attribute)
        if key not in self.temp_save.keys():
            assert False, "未发现key" + key + "在临时保存数据中"
        else:
            if self.temp_save[key] == attribute_value:
                return False
            else:
                return True

    def check_attribute_not_change(self, key, value, attribute):
        if self.check_attribute_change(key, value, attribute):
            return False
        else:
            return True
