#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from module.golable_function import config_reader
from module.selenium_driver import BrowserDriver
from module.web_actions import WebAction
from module.action_import import ActionImport
import os

PATH = os.path.dirname(os.path.abspath(__file__))


class CaseRunner:
    def __init__(self, case_path):
        self.config = config_reader(case_path)
        self.title = self.config["TITLE"]
        self.description = self.config["DESCRIPTION"]
        self.url = self.config["URL"]
        self.actions = self.config["ACTIONS"]
        self.bd = BrowserDriver()
        self.webdriver = self.bd.chrome_browser_driver()
        self.wa = WebAction(self.webdriver)
        self.wa.url(self.url)
        self.ai = ActionImport(self.webdriver)

    def runner(self):
        try:
            self.__runner()
            self.bd.close_chrome_browser_driver()
        except Exception as error:
            error.__init__ = self.bd.close_chrome_browser_driver()
            raise Exception from error

    def __runner(self):
        for action in self.actions:
            self.do_action(action)

    def do_action(self, data):
        action_type = data["TYPE"]
        if "DATA" in data.keys():
            action_data = data["DATA"]
        else:
            action_data = None
        # action_assert = data["ASSERT"]
        # action_assert_type = action_assert["TYPE"]
        # action_assert_data = action_assert["DATA"]
        if isinstance(action_data, dict):
            self.ai.use_function(action_type, action_data)
        else:
            self.ai.use_function(action_type, action_data)
