#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from module.driver_actions import DriverAction


class Customize:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.web_action = DriverAction(webdriver)
