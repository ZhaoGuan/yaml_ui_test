#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from docker_runner.runner import DockerBrowser
import time


class BrowserDriver:
    def __init__(self):
        self.docker_browser = DockerBrowser()
        self.webdriver = None

    def chrome_browser_driver(self):
        port = self.docker_browser.run()
        while self.docker_browser.browser_status() != "running":
            time.sleep(1)
        time.sleep(5)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.binary_location = './chrome'
        self.webdriver = webdriver.Remote(
            command_executor="http://127.0.0.1:{port}/wd/hub".format(port=str(port)),
            desired_capabilities=DesiredCapabilities.CHROME)
        self.webdriver.fullscreen_window()
        return self.webdriver

    def close_chrome_browser_driver(self):
        self.webdriver.quit()
        self.docker_browser.browser_close()
        print("STOP")
