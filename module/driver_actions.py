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


class DriverAction:
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
        """
        等待元素
        :param value: 元素xpath路径
        :return:
        """
        try:
            return self.webdriver_wait.until(EC.presence_of_element_located((By.XPATH, value)))
        except Exception as e:
            with allure.step('未发现元素截图'):
                allure.attach(self.webdriver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
            assert False, "Not Found The Element " + value

    def assert_result(self, result, step_message):
        """
        失败截图判断
        :param result: 输入结构
        :param step_message: 输入错误提示内容
        :return:
        """
        if result is False:
            with allure.step(step_message):
                allure.attach(self.webdriver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)

    def find_element(self, value):
        """
        返回发现的元素
        :param value: 元素xpath路径
        :return: 返回找到的元素
        """
        return self.wait_element(value)

    def get_element_attribute(self, value, attribute):
        """
        获取元素的特定属性
        :param value: 元素xpath路径
        :param attribute: 要获取的属性
        :return:
        """
        element = self.find_element(value)
        return element.get_attribute(attribute)

    def click_element(self, value):
        """
        点击元素操作
        :param value: 元素xpath路径
        :return: 返回元素
        """
        element = self.find_element(value)
        self.find_element(value).click()
        return element

    def send_element(self, value, message):
        """
        对元素进行传值操作，可以进行简单的文件上传
        :param value: 元素xpath路径
        :param message: 需要传入的具体内容，也可以是文件路径
        :return:
        """
        element = self.find_element(value)
        self.find_element(value).send_keys(message)
        return element

    def clear_element(self, value):
        """
        清空输入框内容
        :param value: 元素xpath路径
        :return:
        """
        element = self.find_element(value)
        element.clear()
        return element

    def click_element_change(self, value):
        """
        元素点击后是否发生了变化
        :param value:
        :return:
        """
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
        """
        将元素的属性按照key：value的形式保存到临时存储中
        :param key: 所保存的key
        :param value: 元素xpath路径
        :param attribute: 要获取的属性
        :return:
        """
        attribute_value = self.get_element_attribute(value, attribute)
        if self.temp_save:
            self.temp_save[key] = attribute_value
        else:
            self.temp_save = {key: attribute_value}

    def check_attribute_change(self, key, value, attribute):
        """
        校验元素的属性和之前保存的是否一致
        :param key: 要从临时存储中获取的key
        :param value: 元素xpath路径
        :param attribute: 要获取的属性
        :return:
        """
        attribute_value = self.get_element_attribute(value, attribute)
        if key not in self.temp_save.keys():
            assert False, "未发现key" + key + "在临时保存数据中"
        else:
            if self.temp_save[key] == attribute_value:
                return False
            else:
                return True

    def check_attribute_not_change(self, key, value, attribute):
        """
        校验元素的属性和之前保存的是否不一致
        :param key: 要从临时存储中获取的key
        :param value: 元素xpath路径
        :param attribute: 要获取的属性
        :return:
        """
        if self.check_attribute_change(key, value, attribute):
            return False
        else:
            return True

    """
    web 方法
    """

    def click_accept_alert(self, value):
        """
        web方法，接受弹窗
        :param value: 元素xpath路径
        :return:
        """
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: EC.alert_is_present())
        alert.accept()

    def click_cancel_alert(self, value):
        """
        web方法，点击弹窗的取消
        :param value: 元素xpath路径
        :return:
        """
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: EC.alert_is_present())
        alert.dissmiss()

    def click_send_keys_accept_alert(self, value, message):
        """
        web方法，弹窗输入内容并接受
        :param value: 元素xpath路径
        :param message: 需要输入的内容
        :return:
        """
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: EC.alert_is_present())
        alert.sendKeys(message)
        alert.accept()

    def click_send_keys_cancel_alert(self, value, message):
        """
        web方法，弹窗输入内容并取消
        :param value: 元素xpath路径
        :param message: 需要输入的内容
        :return:
        """
        self.click_element(value)
        alert = self.webdriver_wait.until(lambda x: EC.alert_is_present())
        alert.sendKeys(message)
        alert.dissmiss()

    def switch_iframe(self, value):
        """
        web方法，切换iframe
        :param value: iframe的xpath路径
        :return:
        """
        try:
            self.webdriver_wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, value)))
        except Exception as e:
            with allure.step('未发现元素截图'):
                allure.attach(self.webdriver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
            assert False, "Not Found The iframe " + value

    def switch_default_iframe(self):
        """
        web方法，切换至初始iframe
        :return:
        """
        self.webdriver.switch_to.default_content()

    def switch_default_page(self):
        """
        web方法，切换至初始页面
        :return:
        """
        handles = self.webdriver.window_handles
        self.webdriver.switch_to_window(handles[0])

    def switch_new_page(self):
        """
        web方法，切换至新的页面
        :return:
        """
        handles = self.webdriver.window_handles
        self.webdriver.switch_to_window(handles[1])

    def print_title(self):
        """
        web方法，输入当年页面的title
        :return:
        """
        title = self.webdriver.title
        print("Title is ", title)
        return title

    def assert_title(self, title):
        """
        web方法，校验当前页面是否为所需title
        :param title: 应为title
        :return:
        """
        now_title = self.webdriver.title
        if now_title != title:
            msg = "当前页面title不为：" + title
            self.assert_result(False, msg)
            assert False

    def window_slide(self, begin_px, end_px):
        """
        web方法，页面上下滑动
        :param begin_px: 起始点
        :param end_px: 结束点
        :return:
        """
        js = "window.scrollTo({begin},{end})".format(begin=str(begin_px), end=str(end_px))
        self.webdriver.execute_script(js)

    def window_to_element(self, value):
        """
        web方法，将也面滑动到可见元素位置上
        :param value: 元素xpath路径
        :return:
        """
        element = self.wait_element(value)
        self.webdriver.execute_script("arguments[0].focus();", element)

    """
    以下内容为直接对返回元素进行校验
    """

    def assert_attribute(self, func, attribute, result):
        """
        返回元素的方法其中的一个属性是否等于result
        :param func: 返回element的方法
        :param attribute: 获取的属性
        :param result: 校验的结果
        :return:
        """
        if func.attribut(attribute) != result:
            msg = "元素属性" + attribute + "不为" + str(result)
            self.assert_result(False, msg)
