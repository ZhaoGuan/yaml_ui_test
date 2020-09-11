#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class AppiumDriver:
    def __init__(self, desired_caps):
        self.desired_caps = desired_caps
        self.port = 4723

    def appium_driver(self):
        self.driver = webdriver.Remote('http://127.0.0.1:{port}/wd/hub'.format(port=str(self.port)), self.desired_caps)
        return self.driver

    def close_appium_driver(self):
        self.driver.quit()
